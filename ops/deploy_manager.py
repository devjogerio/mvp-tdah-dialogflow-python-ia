#!/usr/bin/env python3
import argparse
import subprocess
import sys
import logging
import time
import json
from datetime import datetime

"""
Script de Orquestração de Deploy e Manutenção.
Realiza testes, validação de infra e deploy simulado.
"""

# Configuração de Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('deploy.log')
    ]
)
logger = logging.getLogger(__name__)


class DeployManager:
    def __init__(self, env):
        self.env = env
        self.steps_status = {}

    def run_step(self, step_name, command, cwd=None, ignore_errors=False):
        logger.info(f">>> Iniciando etapa: {step_name}")
        start_time = time.time()

        try:
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                cwd=cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            logger.info(f"Saída: {result.stdout.strip()}")
            status = "SUCCESS"
        except subprocess.CalledProcessError as e:
            logger.error(f"Erro na etapa {step_name}: {e.stderr}")
            status = "FAILED"
            # Registra o status detalhado mesmo em caso de falha antes de levantar a exceção
            duration = time.time() - start_time
            self.steps_status[step_name] = {
                "status": status,
                "duration": f"{duration:.2f}s",
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
            if not ignore_errors:
                raise e

        duration = time.time() - start_time
        self.steps_status[step_name] = {
            "status": status,
            "duration": f"{duration:.2f}s",
            "timestamp": datetime.now().isoformat()
        }
        logger.info(
            f"<<< Etapa {step_name} concluída ({status}) em {duration:.2f}s\n")

    def validate_requirements(self):
        self.run_step("Check Python", "python3 --version")
        try:
            self.run_step("Check Terraform", "terraform -version")
            self.has_terraform = True
        except subprocess.CalledProcessError:
            self.has_terraform = False
            logger.warning(
                "Terraform não encontrado. Etapas de infraestrutura serão puladas.")

    def run_tests(self):
        self.run_step("Unit Tests", "python3 -m pytest tests/", cwd=None)

    def validate_infra(self):
        if not getattr(self, 'has_terraform', False):
            logger.info(
                "Pulando validação de infra (Terraform não detectado).")
            self.steps_status["Terraform Init"] = {
                "status": "SKIPPED", "duration": "0s"}
            self.steps_status["Terraform Validate"] = {
                "status": "SKIPPED", "duration": "0s"}
            return

        # Verifica se o diretório infra existe e se o terraform está instalado
        self.run_step("Terraform Init",
                      "terraform init -backend=false", cwd="infra")
        self.run_step("Terraform Validate", "terraform validate", cwd="infra")

    def deploy(self):
        if self.env == 'prod':
            logger.warning("!!! INICIANDO DEPLOY EM PRODUÇÃO !!!")
            time.sleep(2)  # Pausa dramática

        logger.info(f"Simulando deploy para ambiente: {self.env}")
        # Em um cenário real: terraform apply -auto-approve
        self.run_step("Deploy Simulation", "echo 'Deploying resources...'")

    def generate_report(self):
        report_file = f"deploy_report_{self.env}_{int(time.time())}.json"
        with open(report_file, 'w') as f:
            json.dump(self.steps_status, f, indent=2)
        logger.info(f"Relatório gerado em: {report_file}")

        print("\n=== RESUMO DO PROCESSO ===")
        for step, data in self.steps_status.items():
            icon = "✅" if data['status'] == "SUCCESS" else "❌"
            print(f"{icon} {step}: {data['status']} ({data['duration']})")


def main():
    parser = argparse.ArgumentParser(description="TDAH Chatbot Deploy Manager")
    parser.add_argument(
        "--env", choices=['dev', 'prod'], default='dev', help="Ambiente alvo")
    parser.add_argument("--skip-tests", action='store_true',
                        help="Pular testes unitários")

    args = parser.parse_args()

    manager = DeployManager(args.env)

    try:
        manager.validate_requirements()

        if not args.skip_tests:
            manager.run_tests()

        manager.validate_infra()
        manager.deploy()

    except Exception as e:
        logger.critical(f"Processo abortado devido a erro crítico: {str(e)}")
        sys.exit(1)
    finally:
        manager.generate_report()


if __name__ == "__main__":
    main()
