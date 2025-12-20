#!/bin/bash

# ============================================================================
# D0010 SAMPLE FILES GENERATOR
# ============================================================================
# This script creates 10 diverse D0010 sample files for testing the import system
# Usage: bash generate_samples.sh
# ============================================================================

echo "🦑 Generating 10 D0010 Sample Files for Testing..."
echo ""

# Create samples directory if it doesn't exist
mkdir -p sample_data

# Sample 1: Residential properties with smart meters
cat > sample_data/residential_smart_meters.uff << 'EOF'
ZHV|0000475701|D0010002|D|UDMS|X|MRCY|20240115123045||||OPER| | |
026|1400056789012|V| | |
028|SM1A 12345|S| | |
030|01|20240115000000|45123.500|||T|N| | |
030|02|20240115000000|23456.250|||T|N| | |
026|1400056789013|V| | |
028|SM1B 67890|S| | |
030|DY|20240115000000|34567.125|||T|N| | |
030|NT|20240115000000|12345.875|||T|N| | |
026|1400056789014|V| | |
028|SM2C 11111|S| | |
030|S|20240115000000|56789.750|||T|N| | |
ZPT|0000475701|15||5|20240115124500| |
EOF

# Sample 2: Commercial properties with multiple registers
cat > sample_data/commercial_properties.uff << 'EOF'
ZHV|0000475702|D0010002|D|UDMS|X|MRCY|20240201145030||||OPER| | |
026|2100098765432|V| | |
028|C01A 98765|C| | |
030|01|20240201000000|123456.789|||T|N| | |
030|02|20240201000000|234567.890|||T|N| | |
030|03|20240201000000|345678.901|||T|N| | |
026|2200087654321|V| | |
028|C02B 87654|C| | |
030|TO|20240201000000|987654.321|||T|N| | |
026|2300076543210|V| | |
028|C03C 76543|C| | |
030|A1|20240201000000|456789.012|||T|N| | |
ZPT|0000475702|25||6|20240201150015| |
EOF

# Sample 3: Industrial meters with high consumption
cat > sample_data/industrial_meters.uff << 'EOF'
ZHV|0000475703|D0010002|D|UDMS|X|MRCY|20240301092015||||OPER| | |
026|3000012345678|V| | |
028|IND1 54321|D| | |
030|S|20240301000000|1234567.890|||T|N| | |
026|3000023456789|V| | |
028|IND2 65432|D| | |
030|01|20240301000000|2345678.901|||T|N| | |
030|02|20240301000000|3456789.012|||T|N| | |
026|3000034567890|V| | |
028|IND3 76543|D| | |
030|TO|20240301000000|4567890.123|||T|N| | |
026|3000045678901|V| | |
028|IND4 87654|D| | |
030|DY|20240301000000|5678901.234|||T|N| | |
030|NT|20240301000000|6789012.345|||T|N| | |
ZPT|0000475703|35||8|20240301093500| |
EOF

# Sample 4: Prepayment meters
cat > sample_data/prepayment_meters.uff << 'EOF'
ZHV|0000475704|D0010002|D|UDMS|X|MRCY|20240415163022||||OPER| | |
026|1500011111111|V| | |
028|PP01 11111|P| | |
030|S|20240415000000|12345.100|||T|N| | |
026|1500022222222|V| | |
028|PP02 22222|P| | |
030|TO|20240415000000|23456.200|||T|N| | |
026|1500033333333|V| | |
028|PP03 33333|P| | |
030|01|20240415000000|34567.300|||T|N| | |
026|1500044444444|V| | |
028|PP04 44444|P| | |
030|DY|20240415000000|45678.400|||T|N| | |
030|NT|20240415000000|56789.500|||T|N| | |
ZPT|0000475704|40||7|20240415164500| |
EOF

# Sample 5: Mixed meter types - recent readings
cat > sample_data/mixed_recent_readings.uff << 'EOF'
ZHV|0000475705|D0010002|D|UDMS|X|MRCY|20240520180045||||OPER| | |
026|1600088888888|V| | |
028|MX1A 88888|S| | |
030|S|20240520000000|78901.600|||T|N| | |
026|1700099999999|V| | |
028|MX2B 99999|C| | |
030|01|20240520000000|89012.700|||T|N| | |
030|02|20240520000000|90123.800|||T|N| | |
026|1800000000001|V| | |
028|MX3C 00001|D| | |
030|TO|20240520000000|12345.900|||T|N| | |
026|1900000000002|V| | |
028|MX4D 00002|P| | |
030|A1|20240520000000|23456.000|||T|N| | |
026|2000000000003|V| | |
028|MX5E 00003|S| | |
030|WK|20240520000000|34567.100|||T|N| | |
ZPT|0000475705|50||9|20240520181530| |
EOF

# Sample 6: Economy 7 meters (day/night rates)
cat > sample_data/economy7_meters.uff << 'EOF'
ZHV|0000475706|D0010002|D|UDMS|X|MRCY|20240610072030||||OPER| | |
026|1750012345679|V| | |
028|E7A1 12379|S| | |
030|DY|20240610000000|45678.250|||T|N| | |
030|NT|20240610000000|12345.750|||T|N| | |
026|1750023456780|V| | |
028|E7B2 23780|S| | |
030|DY|20240610000000|56789.350|||T|N| | |
030|NT|20240610000000|23456.850|||T|N| | |
026|1750034567891|V| | |
028|E7C3 34891|S| | |
030|DY|20240610000000|67890.450|||T|N| | |
030|NT|20240610000000|34567.950|||T|N| | |
026|1750045678902|V| | |
028|E7D4 45902|S| | |
030|DY|20240610000000|78901.550|||T|N| | |
030|NT|20240610000000|45678.050|||T|N| | |
ZPT|0000475706|60||8|20240610073515| |
EOF

# Sample 7: Small business meters
cat > sample_data/small_business.uff << 'EOF'
ZHV|0000475707|D0010002|D|UDMS|X|MRCY|20240701113045||||OPER| | |
026|2100001234567|V| | |
028|SB01 01234|C| | |
030|01|20240701000000|89012.400|||T|N| | |
026|2100002345678|V| | |
028|SB02 02345|C| | |
030|TO|20240701000000|90123.500|||T|N| | |
026|2100003456789|V| | |
028|SB03 03456|C| | |
030|S|20240701000000|12345.600|||T|N| | |
026|2100004567890|V| | |
028|SB04 04567|C| | |
030|A1|20240701000000|23456.700|||T|N| | |
026|2100005678901|V| | |
028|SB05 05678|C| | |
030|02|20240701000000|34567.800|||T|N| | |
ZPT|0000475707|70||5|20240701114530| |
EOF

# Sample 8: Different date ranges - March readings
cat > sample_data/march_readings.uff << 'EOF'
ZHV|0000475708|D0010002|D|UDMS|X|MRCY|20240315195522||||OPER| | |
026|1650087654321|V| | |
028|MAR1 87654|S| | |
030|S|20240315000000|45123.750|||T|N| | |
026|1650098765432|V| | |
028|MAR2 98765|D| | |
030|01|20240315000000|56234.850|||T|N| | |
030|02|20240315000000|67345.950|||T|N| | |
026|1650009876543|V| | |
028|MAR3 09876|C| | |
030|TO|20240315000000|78456.050|||T|N| | |
026|1650010987654|V| | |
028|MAR4 10987|P| | |
030|DY|20240315000000|89567.150|||T|N| | |
030|NT|20240315000000|90678.250|||T|N| | |
026|1650021098765|V| | |
028|MAR5 21098|S| | |
030|A1|20240315000000|12789.350|||T|N| | |
ZPT|0000475708|80||7|20240315200530| |
EOF

# Sample 9: High-frequency readings (multiple times same day)
cat > sample_data/multiple_daily_readings.uff << 'EOF'
ZHV|0000475709|D0010002|D|UDMS|X|MRCY|20240801141530||||OPER| | |
026|1850001111222|V| | |
028|HF01 11222|S| | |
030|S|20240801060000|23456.100|||T|N| | |
030|S|20240801120000|23458.200|||T|N| | |
030|S|20240801180000|23460.300|||T|N| | |
026|1850002222333|V| | |
028|HF02 22333|C| | |
030|01|20240801060000|34567.400|||T|N| | |
030|02|20240801060000|45678.500|||T|N| | |
030|01|20240801180000|34570.600|||T|N| | |
030|02|20240801180000|45682.700|||T|N| | |
026|1850003333444|V| | |
028|HF03 33444|D| | |
030|TO|20240801120000|56789.800|||T|N| | |
ZPT|0000475709|90||6|20240801142515| |
EOF

# Sample 10: Various register types showcase
cat > sample_data/register_showcase.uff << 'EOF'
ZHV|0000475710|D0010002|D|UDMS|X|MRCY|20240901221045||||OPER| | |
026|1950088776655|V| | |
028|REG1 88776|S| | |
030|01|20240901000000|11111.111|||T|N| | |
030|02|20240901000000|22222.222|||T|N| | |
030|03|20240901000000|33333.333|||T|N| | |
026|1950099887766|V| | |
028|REG2 99887|C| | |
030|S|20240901000000|44444.444|||T|N| | |
030|TO|20240901000000|55555.555|||T|N| | |
026|1950000998877|V| | |
028|REG3 00998|D| | |
030|A1|20240901000000|66666.666|||T|N| | |
030|DY|20240901000000|77777.777|||T|N| | |
030|NT|20240901000000|88888.888|||T|N| | |
026|1950011009988|V| | |
028|REG4 11009|P| | |
030|WK|20240901000000|99999.999|||T|N| | |
030|OT|20240901000000|10101.010|||T|N| | |
ZPT|0000475710|100||8|20240901222530| |
EOF

echo "✅ Successfully created 10 sample D0010 files:"
echo ""
echo "📄 1. residential_smart_meters.uff    - Smart meters in homes (5 readings)"
echo "📄 2. commercial_properties.uff       - Business properties (6 readings)" 
echo "📄 3. industrial_meters.uff           - High-consumption industrial (8 readings)"
echo "📄 4. prepayment_meters.uff           - Prepayment meter types (7 readings)"
echo "📄 5. mixed_recent_readings.uff       - Mixed meter types, recent (9 readings)"
echo "📄 6. economy7_meters.uff             - Day/night tariff meters (8 readings)"
echo "📄 7. small_business.uff              - Small business meters (5 readings)"
echo "📄 8. march_readings.uff              - March 2024 readings (7 readings)"
echo "📄 9. multiple_daily_readings.uff     - Multiple readings per day (6 readings)"
echo "📄 10. register_showcase.uff          - All register types demo (8 readings)"
echo ""
echo "📊 Total: 69 unique meter readings across 10 files"
echo ""
echo "🚀 Import commands to test:"
echo ""
echo "# Import all files at once:"
echo "python manage.py import_d0010 sample_data/*.uff"
echo ""
echo "# Import individual files:"
echo "python manage.py import_d0010 sample_data/residential_smart_meters.uff"
echo "python manage.py import_d0010 sample_data/commercial_properties.uff"
echo "python manage.py import_d0010 sample_data/industrial_meters.uff"
echo "python manage.py import_d0010 sample_data/prepayment_meters.uff"
echo "python manage.py import_d0010 sample_data/mixed_recent_readings.uff"
echo "python manage.py import_d0010 sample_data/economy7_meters.uff"
echo "python manage.py import_d0010 sample_data/small_business.uff"
echo "python manage.py import_d0010 sample_data/march_readings.uff"
echo "python manage.py import_d0010 sample_data/multiple_daily_readings.uff"
echo "python manage.py import_d0010 sample_data/register_showcase.uff"
echo ""
echo "🎯 Demo searches to try in admin:"
echo ""
echo "MPANs to search for:"
echo "• 1400056789012 (smart meter)"
echo "• 2100098765432 (commercial)" 
echo "• 3000012345678 (industrial)"
echo "• 1500011111111 (prepayment)"
echo ""
echo "Meter serials to search for:"
echo "• SM1A 12345 (smart meter)"
echo "• C01A 98765 (commercial)"
echo "• IND1 54321 (industrial)"
echo "• PP01 11111 (prepayment)"
echo ""
echo "🦑 Ready for comprehensive testing!"
