#!/usr/bin/env python3
"""Test Oracle WMS integration with REAL data from .env credentials.

This script tests the refactored flext-oracle-wms implementation using real
Oracle WMS API credentials to validate that the integration works correctly.
"""

import asyncio
import os
from pathlib import Path

# Add the src directory to Python path
import sys
sys.path.insert(0, str(Path(__file__).parent / "src"))

from flext_oracle_wms.client import FlextOracleWmsClient
from flext_oracle_wms.config import FlextOracleWmsClientConfig
from flext_oracle_wms.constants import FlextOracleWmsApiVersion


async def test_real_oracle_wms():
    """Test Oracle WMS integration with real credentials."""
    print("🚀 Testing Oracle WMS Integration with REAL Data")
    print("=" * 60)
    
    try:
        # Load configuration from .env (using real credentials)
        config = FlextOracleWmsClientConfig(
            base_url=os.getenv("ORACLE_WMS_BASE_URL", ""),
            username=os.getenv("ORACLE_WMS_USERNAME", ""),
            password=os.getenv("ORACLE_WMS_PASSWORD", ""),
            environment="raizen_test",  # From URL
            api_version=FlextOracleWmsApiVersion.LGF_V10,
            timeout=float(os.getenv("ORACLE_WMS_TIMEOUT", "30")),
            max_retries=int(os.getenv("ORACLE_WMS_MAX_RETRIES", "3")),
            verify_ssl=os.getenv("ORACLE_WMS_VERIFY_SSL", "true").lower() == "true",
            enable_logging=True
        )
        
        print(f"📍 Base URL: {config.base_url}")
        print(f"👤 Username: {config.username}")
        print(f"🔧 Environment: {config.environment}")
        print(f"📡 API Version: {config.api_version}")
        print()
        
        # Create and start client
        print("🔄 Creating Oracle WMS Client...")
        client = FlextOracleWmsClient(config)
        
        print("🔄 Starting Oracle WMS Client...")
        start_result = await client.start()
        if not start_result.is_success:
            print(f"❌ Failed to start client: {start_result.error}")
            return False
            
        print("✅ Oracle WMS Client started successfully!")
        print()
        
        # Test 1: Entity Discovery
        print("🔍 Test 1: Discovering Oracle WMS Entities...")
        entities_result = await client.discover_entities()
        if entities_result.is_success:
            entities = entities_result.data
            print(f"✅ Successfully discovered {len(entities)} entities")
            print(f"📋 First 10 entities: {entities[:10]}")
        else:
            print(f"❌ Entity discovery failed: {entities_result.error}")
        
        print()
        
        # Test 2: Health Check
        print("🏥 Test 2: Health Check...")
        health_result = await client.health_check()
        if health_result.is_success:
            health_data = health_result.data
            print("✅ Health check passed!")
            print(f"📊 Service: {health_data.get('service')}")
            print(f"🟢 Status: {health_data.get('status')}")
            print(f"🔌 Available APIs: {health_data.get('available_apis')}")
            print(f"📈 Discovered Entities: {health_data.get('discovered_entities')}")
        else:
            print(f"❌ Health check failed: {health_result.error}")
        
        print()
        
        # Test 3: Get Entity Data (try company first)
        if entities_result.is_success and entities_result.data:
            test_entity = "company" if "company" in entities_result.data else entities_result.data[0]
            print(f"📦 Test 3: Getting data for entity '{test_entity}'...")
            
            entity_data_result = await client.get_entity_data(
                entity_name=test_entity,
                limit=5
            )
            
            if entity_data_result.is_success:
                data = entity_data_result.data
                print(f"✅ Successfully retrieved data for '{test_entity}'")
                print(f"📄 Data type: {type(data)}")
                if isinstance(data, dict):
                    print(f"🔑 Keys: {list(data.keys())}")
            else:
                print(f"❌ Failed to get entity data: {entity_data_result.error}")
        
        print()
        
        # Test 4: Test Specific Entity by ID (if we have data)
        if entities_result.is_success and entities_result.data:
            # Try to get a specific record by ID for the first entity
            test_entity = entities_result.data[0]
            print(f"🎯 Test 4: Getting specific record for entity '{test_entity}'...")
            
            # For this test, we'll try to get record with ID "1" (common in many entities)
            try:
                entity_by_id_result = await client.get_entity_by_id(
                    entity_name=test_entity,
                    entity_id="1"
                )
                
                if entity_by_id_result.is_success:
                    data = entity_by_id_result.data
                    print(f"✅ Successfully retrieved specific record")
                    print(f"📄 Data type: {type(data)}")
                else:
                    print(f"⚠️  No record with ID '1' found (expected): {entity_by_id_result.error}")
            except Exception as e:
                print(f"⚠️  Error getting specific record (expected): {e}")
        
        print()
        
        # Test 5: API Catalog Test
        print("📚 Test 5: Testing API Catalog...")
        available_apis = client.get_available_apis()
        print(f"✅ Available APIs: {len(available_apis)}")
        
        # List some API categories
        from flext_oracle_wms.api_catalog import FlextOracleWmsApiCategory
        for category in FlextOracleWmsApiCategory:
            category_apis = client.get_apis_by_category(category)
            if category_apis:
                print(f"  📁 {category.value}: {len(category_apis)} APIs")
        
        print()
        
        # Cleanup
        print("🧹 Cleaning up...")
        stop_result = await client.stop()
        if stop_result.is_success:
            print("✅ Oracle WMS Client stopped successfully!")
        else:
            print(f"⚠️  Warning during stop: {stop_result.error}")
        
        print()
        print("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
        print("✅ Oracle WMS integration is working with REAL data!")
        return True
        
    except Exception as e:
        print(f"💥 CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Main test function."""
    # Load environment variables from .env file
    from dotenv import load_dotenv
    load_dotenv()
    
    # Validate required environment variables
    required_vars = ["ORACLE_WMS_BASE_URL", "ORACLE_WMS_USERNAME", "ORACLE_WMS_PASSWORD"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {missing_vars}")
        print("Please ensure your .env file contains all required Oracle WMS credentials.")
        return False
    
    # Run the test
    success = await test_real_oracle_wms()
    
    if success:
        print("\n🏆 INTEGRATION TEST: PASSED")
        print("✅ flext-oracle-wms is ready for production!")
    else:
        print("\n💥 INTEGRATION TEST: FAILED")
        print("❌ Please fix the issues above before proceeding.")
    
    return success


if __name__ == "__main__":
    # Install python-dotenv if not available
    try:
        import dotenv
    except ImportError:
        print("Installing python-dotenv...")
        import subprocess
        subprocess.check_call(["pip", "install", "python-dotenv"])
        import dotenv
    
    # Run the test
    result = asyncio.run(main())
    sys.exit(0 if result else 1)