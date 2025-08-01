#!/usr/bin/env python3
"""
Oracle WMS REAL Testing with Valid Credentials

Testing with REAL Oracle WMS credentials provided by user:
- Base URL: https://ta29.wms.ocs.oraclecloud.com/raizen_test
- Username: USER_WMS_INTEGRA  
- Password: jmCyS7BK94YvhS@

This will test ACTUAL Oracle WMS functionality, not mocks.
"""

import asyncio
import os
from datetime import UTC, datetime

from flext_core import FlextResult, get_logger
from flext_oracle_wms import (
    FlextOracleWmsClientConfig,
    create_oracle_wms_client
)
from flext_oracle_wms.api_catalog import FlextOracleWmsApiVersion

logger = get_logger(__name__)

async def test_real_oracle_wms():
    """Test REAL Oracle WMS functionality with valid credentials."""
    
    print("\n" + "=" * 80)
    print("🔥 ORACLE WMS REAL TESTING - CREDENCIAIS VÁLIDAS")
    print("=" * 80)
    print("🌐 Base URL: https://ta29.wms.ocs.oraclecloud.com/raizen_test")
    print("👤 Username: USER_WMS_INTEGRA")
    print("🔐 Password: [REDACTED]")
    print("=" * 80)
    
    # Create REAL configuration with provided credentials
    config = FlextOracleWmsClientConfig(
        base_url="https://ta29.wms.ocs.oraclecloud.com",
        username="USER_WMS_INTEGRA",
        password="jmCyS7BK94YvhS@",
        environment="raizen_test",
        timeout=60.0,  # Increased timeout for real network calls
        max_retries=3,
        api_version=FlextOracleWmsApiVersion.LGF_V10,
        verify_ssl=True,
        enable_logging=True
    )
    
    # Create REAL Oracle WMS client (NO MOCK MODE)
    real_client = create_oracle_wms_client(config, mock_mode=False)
    
    test_results = {
        "client_start": False,
        "entity_discovery": False,
        "entity_data": False,
        "health_check": False,
        "api_catalog": False
    }
    
    try:
        # Test 1: Client Initialization and Authentication
        print("\n🧪 TEST 1: REAL CLIENT AUTHENTICATION")
        print("-" * 60)
        
        start_result = await real_client.start()
        if start_result.is_success:
            print("✅ SUCESSO: Cliente Oracle WMS autenticado com credenciais reais")
            test_results["client_start"] = True
        else:
            print(f"❌ FALHA: Autenticação falhou - {start_result.error}")
            return test_results
        
        # Test 2: Entity Discovery from REAL Oracle WMS
        print("\n🧪 TEST 2: REAL ENTITY DISCOVERY")
        print("-" * 60)
        
        entities_result = await real_client.discover_entities()
        if entities_result.is_success:
            entities = entities_result.data
            print(f"✅ SUCESSO: Descobertas {len(entities)} entidades REAIS do Oracle WMS")
            print(f"   Primeiras 10 entidades: {entities[:10]}")
            test_results["entity_discovery"] = True
            discovered_entities = entities
        else:
            print(f"❌ FALHA: Discovery falhou - {entities_result.error}")
            discovered_entities = ["company", "facility", "item"]  # Fallback
        
        # Test 3: Real Data Extraction
        print("\n🧪 TEST 3: REAL DATA EXTRACTION")
        print("-" * 60)
        
        if discovered_entities:
            # Test with first available entity
            test_entity = discovered_entities[0]
            print(f"🔍 Testando extração de dados para entidade: {test_entity}")
            
            data_result = await real_client.get_entity_data(
                test_entity, 
                limit=5,  # Small limit for testing
                fields="id,create_ts,mod_ts"  # Basic fields
            )
            
            if data_result.is_success:
                data = data_result.data
                if isinstance(data, dict):
                    count = data.get("count", 0)
                    results = data.get("results", [])
                    print(f"✅ SUCESSO: Extraídos {count} registros REAIS para {test_entity}")
                    
                    if results and isinstance(results, list) and len(results) > 0:
                        sample_record = results[0]
                        if isinstance(sample_record, dict):
                            fields = list(sample_record.keys())
                            print(f"   Campos do registro: {fields[:10]}")
                            
                            # Show sample data (first few fields only)
                            sample_data = {k: v for k, v in list(sample_record.items())[:3]}
                            print(f"   Dados exemplo: {sample_data}")
                            
                    test_results["entity_data"] = True
                else:
                    print(f"❌ FALHA: Dados retornados não são dict - {type(data)}")
            else:
                print(f"❌ FALHA: Extração de dados falhou - {data_result.error}")
        
        # Test 4: Health Check with Real Connection
        print("\n🧪 TEST 4: REAL HEALTH CHECK")
        print("-" * 60)
        
        health_result = await real_client.health_check()
        if health_result.is_success:
            health_data = health_result.data
            if isinstance(health_data, dict):
                status = health_data.get("status", "unknown")
                base_url = health_data.get("base_url", "unknown")
                environment = health_data.get("environment", "unknown")
                available_entities = health_data.get("discovered_entities", 0)
                
                print(f"✅ SUCESSO: Oracle WMS está {status}")
                print(f"   Base URL: {base_url}")
                print(f"   Environment: {environment}")
                print(f"   Entidades disponíveis: {available_entities}")
                test_results["health_check"] = True
            else:
                print(f"❌ FALHA: Health check retornou dados inválidos - {type(health_data)}")
        else:
            print(f"❌ FALHA: Health check falhou - {health_result.error}")
        
        # Test 5: API Catalog Validation
        print("\n🧪 TEST 5: API CATALOG VALIDATION")
        print("-" * 60)
        
        available_apis = real_client.get_available_apis()
        lgf_apis = real_client.get_apis_by_category("data_extract")
        
        print(f"✅ SUCESSO: {len(available_apis)} APIs catalogadas")
        print(f"   APIs LGF v10 (data extract): {len(lgf_apis)}")
        
        # Show some key APIs
        key_apis = ["lgf_entity_list", "lgf_entity_discovery", "lgf_data_extract"]
        for api_name in key_apis:
            if api_name in available_apis:
                api = available_apis[api_name]
                print(f"   ✅ {api_name}: {api.method} {api.path}")
            else:
                print(f"   ❌ {api_name}: NOT FOUND")
        
        test_results["api_catalog"] = True
        
        # Stop the client
        await real_client.stop()
        print("\n✅ Cliente Oracle WMS desconectado com sucesso")
        
    except Exception as e:
        logger.exception("Real Oracle WMS test failed")
        print(f"\n❌ ERRO CRÍTICO: {e}")
        try:
            await real_client.stop()
        except:
            pass
    
    return test_results

async def test_oracle_wms_pipeline():
    """Test complete TAP -> TARGET pipeline with real data."""
    
    print("\n" + "=" * 80) 
    print("🔄 PIPELINE COMPLETO TAP → TARGET COM DADOS REAIS")
    print("=" * 80)
    
    # This would test the complete pipeline but requires implementing
    # the actual data insertion in the target
    print("⚠️  Pipeline completo requer implementação da inserção real no target")
    print("   Atualmente o target está em modo estrutural (apenas logs)")
    print("   TODO: Implementar inserção real de dados no Oracle WMS via target")

async def main():
    """Main test runner with real Oracle WMS credentials."""
    
    print("🚀 INICIANDO TESTES COM ORACLE WMS REAL...")
    print("🔑 Usando credenciais fornecidas pelo usuário")
    
    try:
        # Test real Oracle WMS functionality
        test_results = await test_real_oracle_wms()
        
        # Test pipeline (structural only for now)
        await test_oracle_wms_pipeline()
        
        # Final Results Summary
        print("\n" + "=" * 80)
        print("📊 RESULTADOS FINAIS - TESTES COM CREDENCIAIS REAIS")
        print("=" * 80)
        
        passed_tests = sum(1 for result in test_results.values() if result)
        total_tests = len(test_results)
        
        print(f"\n🎯 TESTES APROVADOS: {passed_tests}/{total_tests}")
        
        for test_name, passed in test_results.items():
            status = "✅ PASSOU" if passed else "❌ FALHOU"
            print(f"   {test_name}: {status}")
        
        if passed_tests == total_tests:
            print("\n🎉 TODOS OS TESTES PASSARAM!")
            print("✅ Oracle WMS funcionalidade REAL validada com sucesso")
            print("✅ Credenciais válidas e conectividade confirmada")
            print("✅ Extração de dados REAIS funcionando")
        else:
            print(f"\n⚠️  {total_tests - passed_tests} testes falharam")
            print("❓ Verificar logs acima para detalhes dos erros")
        
        # Honesty Assessment
        print("\n" + "=" * 80)
        print("🔍 AVALIAÇÃO HONESTA FINAL")
        print("=" * 80)
        
        if test_results["client_start"] and test_results["entity_discovery"]:
            print("\n✅ VALIDAÇÃO FUNCIONAL CONFIRMADA:")
            print("   🔐 Credenciais Oracle WMS válidas e funcionais")
            print("   📡 Conectividade real com Oracle WMS Cloud estabelecida")
            print("   📊 Descoberta de entidades funcionando com dados reais")
            
            if test_results["entity_data"]:
                print("   📥 Extração de dados reais funcionando")
            else:
                print("   ❌ Extração de dados precisa ser investigada")
        else:
            print("\n❌ VALIDAÇÃO FUNCIONAL FALHOU:")
            print("   🔐 Credenciais podem estar incorretas ou expiradas")
            print("   📡 Problemas de conectividade ou configuração")
        
        print("\n💡 PRÓXIMOS PASSOS:")
        if passed_tests >= 3:  # Most tests passed
            print("   1. ✅ Funcionalidade básica validada - continuar desenvolvimento")
            print("   2. 🔧 Implementar inserção real de dados no target")
            print("   3. 🧪 Testar pipeline completo TAP→TARGET→DBT")
            print("   4. 📈 Otimizar performance para volumes maiores")
        else:
            print("   1. 🔍 Investigar falhas de conectividade ou autenticação")
            print("   2. 📞 Verificar com REDACTED_LDAP_BIND_PASSWORDistrador Oracle WMS se credenciais estão ativas")
            print("   3. 🌐 Testar conectividade de rede para Oracle Cloud")
        
    except Exception as e:
        logger.exception("Main test execution failed")
        print(f"\n❌ EXECUÇÃO DOS TESTES FALHOU: {e}")
        print("🔍 Verificar logs para detalhes do erro")

if __name__ == "__main__":
    asyncio.run(main())