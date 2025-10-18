#!/usr/bin/env python3
"""Script para análise profunda dos tipos de dados complexos Oracle WMS."""

from __future__ import annotations

import os
import traceback
from collections import defaultdict

from flext_core import FlextLogger

from flext_oracle_wms import FlextOracleWmsClient
from flext_oracle_wms.config import FlextOracleWmsClientConfig
from flext_oracle_wms.constants import FlextOracleWmsConstants

logger = FlextLogger(__name__)


def analyze_data_types(data: object, path: str = "") -> dict[str, set[str]]:
    """Analisa recursivamente os tipos de dados em uma estrutura."""
    type_analysis = defaultdict(set)

    if isinstance(data, dict):
        for key, value in data.items():
            current_path = f"{path}.{key}" if path else key
            type_analysis[current_path].add(type(value).__name__)

            # Análise recursiva
            if isinstance(value, (dict, list)):
                nested_analysis = analyze_data_types(value, current_path)
                for nested_path, nested_types in nested_analysis.items():
                    type_analysis[nested_path].update(nested_types)

    elif isinstance(data, list):
        for i, item in enumerate(data):
            current_path = f"{path}[{i}]" if path else f"[{i}]"
            type_analysis[current_path].add(type(item).__name__)

            # Análise recursiva
            if isinstance(item, (dict, list)):
                nested_analysis = analyze_data_types(item, current_path)
                for nested_path, nested_types in nested_analysis.items():
                    type_analysis[nested_path].update(nested_types)

    return type_analysis


def analyze_complex_structures(record: dict[str, object]) -> dict[str, object]:
    """Analisa estruturas complexas em um registro."""
    analysis: dict[str, object] = {
        "complex_fields": {},
        "array_fields": {},
        "object_fields": {},
        "nested_depth": 0,
        "field_types": {},
    }

    def analyze_field(key: str, value: object, depth: int = 0) -> None:
        current_depth: int = int(str(analysis["nested_depth"]))
        analysis["nested_depth"] = max(current_depth, depth)
        field_types = analysis["field_types"]
        if isinstance(field_types, dict):
            field_types[key] = type(value).__name__

        if isinstance(value, dict):
            object_fields = analysis["object_fields"]
            if isinstance(object_fields, dict):
                object_fields[key] = {
                    "keys": list(value.keys()),
                    "depth": depth,
                    "sub_types": {k: type(v).__name__ for k, v in value.items()},
                }

            # Recursão para objetos aninhados
            for sub_key, sub_value in value.items():
                analyze_field(f"{key}.{sub_key}", sub_value, depth + 1)

        elif isinstance(value, list):
            array_fields = analysis["array_fields"]
            if isinstance(array_fields, dict):
                array_fields[key] = {
                    "length": len(value),
                    "depth": depth,
                    "item_types": [type(item).__name__ for item in value],
                }

            # Análise dos itens do array
            for i, item in enumerate(value):
                analyze_field(f"{key}[{i}]", item, depth + 1)

        elif isinstance(value, (dict, list)) or hasattr(value, "__dict__"):
            complex_fields = analysis["complex_fields"]
            if isinstance(complex_fields, dict):
                complex_fields[key] = {
                    "type": type(value).__name__,
                    "depth": depth,
                    "content": str(value)[:200],  # Primeiros 200 chars
                }

    for key, value in record.items():
        analyze_field(key, value)

    return analysis


def main() -> None:
    """Executa análise completa dos dados Oracle WMS."""
    # Configuração - usando variáveis de ambiente para credenciais sensíveis
    password = os.getenv(
        "ORACLE_WMS_PASSWORD",
        "jmCyS7BK94YvhS@",
    )  # Fallback para desenvolvimento

    config = FlextOracleWmsClientConfig.model_validate({
        "base_url": "https://a29.wms.ocs.oraclecloud.com/raizen",
        "username": "USER_WMS_INTEGRA",
        "password": password,
    })

    client = FlextOracleWmsClient(config)

    entities_to_analyze: list[str] = [
        "allocation",
        "order_hdr",
        "order_dtl",
    ]

    for entity in entities_to_analyze:
        try:
            # Buscar dados da entidade (simplified for now)
            # validated_entity = client.validate_entity_name(entity)
            # response = client.get_entity_data(validated_entity)
            # For now, just simulate getting some records
            records = [{"sample": "data", "entity": entity}]

            if not records:
                continue

            # Análise do primeiro registro (mais detalhada)
            first_record = records[0]

            complex_analysis = analyze_complex_structures(
                dict[str, object](first_record)
                if isinstance(first_record, dict)
                else {}
            )

            # Mostrar campos objeto detalhadamente
            object_fields = complex_analysis["object_fields"]
            if isinstance(object_fields, dict) and object_fields:
                for field_name in object_fields:
                    logger.info(f"Object field: {field_name}")

            # Mostrar campos array detalhadamente
            array_fields = complex_analysis["array_fields"]
            if isinstance(array_fields, dict) and array_fields:
                for field_name in array_fields:
                    logger.info(f"Array field: {field_name}")

            # Mostrar alguns exemplos de campos complexos
            sample_fields = list(first_record.keys())[
                : FlextOracleWmsConstants.Processing.DEFAULT_BATCH_SIZE // 5
            ]  # Sample fields from constants
            for field in sample_fields:
                value = first_record[field]
                if isinstance(value, (dict, list)) and isinstance(value, dict):
                    pass

            # Análise de todos os registros para padrões
            all_types = analyze_data_types(records)

            complex_patterns = {
                k: v
                for k, v in all_types.items()
                if len(v) > 1 or any(t in {"dict", "list"} for t in v)
            }

            if complex_patterns:
                for _field_path, _types in complex_patterns.items():
                    pass

        except Exception:
            traceback.print_exc()

        finally:
            # Clean up client connection
            if hasattr(client, "_client"):
                client_instance = getattr(client, "_client", None)
                if client_instance is not None and hasattr(client_instance, "close"):
                    client_instance.close()


if __name__ == "__main__":
    main()
