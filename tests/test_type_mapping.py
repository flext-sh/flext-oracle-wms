"""Test Oracle WMS type mapping functionality."""


from flext_oracle_wms.type_mapping import (
    FLEXT_ORACLE_WMS_FIELD_PATTERNS,
    FLEXT_ORACLE_WMS_TYPE_MAPPINGS,
    FlextOracleWmsTypeMapper,
    flext_oracle_wms_create_type_mapper,
    flext_oracle_wms_map_oracle_to_singer,
)


def test_type_mapper_creation() -> None:
    """Test type mapper creation."""
    mapper = FlextOracleWmsTypeMapper()
    assert isinstance(mapper, FlextOracleWmsTypeMapper)


def test_oracle_type_mapping_varchar() -> None:
    """Test VARCHAR type mapping."""
    mapper = FlextOracleWmsTypeMapper()
    result = mapper.flext_oracle_wms_map_oracle_type("varchar")
    assert result.is_success is True
    assert result.data["type"] == ["string", "null"]


def test_oracle_type_mapping_number() -> None:
    """Test NUMBER type mapping."""
    mapper = FlextOracleWmsTypeMapper()
    result = mapper.flext_oracle_wms_map_oracle_type("number")
    assert result.is_success is True
    assert result.data["type"] == ["number", "null"]


def test_oracle_type_mapping_integer() -> None:
    """Test INTEGER type mapping."""
    mapper = FlextOracleWmsTypeMapper()
    result = mapper.flext_oracle_wms_map_oracle_type("integer")
    assert result.is_success is True
    assert result.data["type"] == ["integer", "null"]


def test_oracle_type_mapping_date() -> None:
    """Test DATE type mapping."""
    mapper = FlextOracleWmsTypeMapper()
    result = mapper.flext_oracle_wms_map_oracle_type("date")
    assert result.is_success is True
    assert result.data["type"] == ["string", "null"]
    assert result.data["format"] == "date"


def test_oracle_type_mapping_timestamp() -> None:
    """Test TIMESTAMP type mapping."""
    mapper = FlextOracleWmsTypeMapper()
    result = mapper.flext_oracle_wms_map_oracle_type("timestamp")
    assert result.is_success is True
    assert result.data["type"] == ["string", "null"]
    assert result.data["format"] == "date-time"


def test_oracle_type_mapping_boolean() -> None:
    """Test BOOLEAN type mapping."""
    mapper = FlextOracleWmsTypeMapper()
    result = mapper.flext_oracle_wms_map_oracle_type("boolean")
    assert result.is_success is True
    assert result.data["type"] == ["boolean", "null"]


def test_oracle_type_mapping_parameterized() -> None:
    """Test parameterized type mapping like VARCHAR(255)."""
    mapper = FlextOracleWmsTypeMapper()
    result = mapper.flext_oracle_wms_map_oracle_type("varchar(255)")
    assert result.is_success is True
    assert result.data["type"] == ["string", "null"]


def test_oracle_type_mapping_unknown() -> None:
    """Test unknown type mapping."""
    mapper = FlextOracleWmsTypeMapper()
    result = mapper.flext_oracle_wms_map_oracle_type("unknown_type")
    assert result.is_success is True
    assert result.data["type"] == ["string", "null"]


def test_field_name_mapping_id() -> None:
    """Test field name mapping for ID fields."""
    mapper = FlextOracleWmsTypeMapper()
    result = mapper.flext_oracle_wms_map_field_by_name("user_id")
    assert result.is_success is True
    assert result.data["type"] == ["integer", "null"]


def test_field_name_mapping_code() -> None:
    """Test field name mapping for CODE fields."""
    mapper = FlextOracleWmsTypeMapper()
    result = mapper.flext_oracle_wms_map_field_by_name("item_code")
    assert result.is_success is True
    assert result.data["type"] == ["string", "null"]


def test_field_name_mapping_date() -> None:
    """Test field name mapping for DATE fields."""
    mapper = FlextOracleWmsTypeMapper()
    result = mapper.flext_oracle_wms_map_field_by_name("created_date")
    assert result.is_success is True
    assert result.data["type"] == ["string", "null"]
    assert result.data["format"] == "date"


def test_field_name_mapping_flag() -> None:
    """Test field name mapping for FLAG fields."""
    mapper = FlextOracleWmsTypeMapper()
    result = mapper.flext_oracle_wms_map_field_by_name("active_flag")
    assert result.is_success is True
    assert result.data["type"] == ["boolean", "null"]


def test_field_name_mapping_count() -> None:
    """Test field name mapping for COUNT fields."""
    mapper = FlextOracleWmsTypeMapper()
    result = mapper.flext_oracle_wms_map_field_by_name("item_count")
    assert result.is_success is True
    assert result.data["type"] == ["integer", "null"]


def test_field_name_mapping_amount() -> None:
    """Test field name mapping for AMOUNT fields."""
    mapper = FlextOracleWmsTypeMapper()
    result = mapper.flext_oracle_wms_map_field_by_name("total_amount")
    assert result.is_success is True
    assert result.data["type"] == ["number", "null"]


def test_schema_field_mapping_with_type() -> None:
    """Test complete schema field mapping with Oracle type."""
    mapper = FlextOracleWmsTypeMapper()
    result = mapper.flext_oracle_wms_map_schema_field(
        field_name="user_id", oracle_type="number",
    )
    assert result.is_success is True
    assert result.data["type"] == ["number", "null"]


def test_schema_field_mapping_nullable() -> None:
    """Test schema field mapping with nullable parameter."""
    mapper = FlextOracleWmsTypeMapper()
    result = mapper.flext_oracle_wms_map_schema_field(
        field_name="user_id", oracle_type="number", nullable=False,
    )
    assert result.is_success is True
    assert "null" not in result.data["type"]


def test_custom_mapping() -> None:
    """Test adding custom type mapping."""
    mapper = FlextOracleWmsTypeMapper()
    custom_schema = {"type": ["string"], "format": "custom"}
    result = mapper.flext_oracle_wms_add_custom_mapping("custom_type", custom_schema)
    assert result.is_success is True

    # Test using the custom mapping
    mapped_result = mapper.flext_oracle_wms_map_oracle_type("custom_type")
    assert mapped_result.is_success is True
    assert mapped_result.data["format"] == "custom"


def test_supported_types() -> None:
    """Test getting supported types."""
    mapper = FlextOracleWmsTypeMapper()
    types = mapper.flext_oracle_wms_get_supported_types()
    assert isinstance(types, list)
    assert "varchar" in types
    assert "number" in types
    assert "integer" in types


def test_factory_function() -> None:
    """Test type mapper factory function."""
    mapper = flext_oracle_wms_create_type_mapper()
    assert isinstance(mapper, FlextOracleWmsTypeMapper)


def test_utility_function() -> None:
    """Test utility mapping function."""
    result = flext_oracle_wms_map_oracle_to_singer("varchar")
    assert result["type"] == ["string", "null"]


def test_type_mappings_constant() -> None:
    """Test type mappings constant."""
    assert isinstance(FLEXT_ORACLE_WMS_TYPE_MAPPINGS, dict)
    assert "varchar" in FLEXT_ORACLE_WMS_TYPE_MAPPINGS
    assert "number" in FLEXT_ORACLE_WMS_TYPE_MAPPINGS


def test_field_patterns_constant() -> None:
    """Test field patterns constant."""
    assert isinstance(FLEXT_ORACLE_WMS_FIELD_PATTERNS, dict)
    assert any("_id$" in pattern for pattern in FLEXT_ORACLE_WMS_FIELD_PATTERNS)
    assert any("_date$" in pattern for pattern in FLEXT_ORACLE_WMS_FIELD_PATTERNS)


def test_case_insensitive_mapping() -> None:
    """Test case-insensitive type mapping."""
    mapper = FlextOracleWmsTypeMapper()
    result1 = mapper.flext_oracle_wms_map_oracle_type("VARCHAR")
    result2 = mapper.flext_oracle_wms_map_oracle_type("varchar")
    assert result1.is_success is True
    assert result2.is_success is True
    assert result1.data == result2.data


def test_field_name_no_match() -> None:
    """Test field name mapping with no pattern match."""
    mapper = FlextOracleWmsTypeMapper()
    result = mapper.flext_oracle_wms_map_field_by_name("random_field")
    assert result.is_success is True
    assert result.data["type"] == ["string", "null"]
