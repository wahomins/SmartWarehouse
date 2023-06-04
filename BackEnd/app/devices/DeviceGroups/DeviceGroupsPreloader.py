from .device_group import DeviceGroup
from .device_sub_group import DeviceSubGroup

def preload_groups():
    groups = [
        {
            'name': 'Access Control',
            'description': 'Access control functionality group'
        },
        {
            'name': 'Safety Monitoring',
            'description': 'Safety monitoring functionality group'
        },
        {
            'name': 'Environmental Monitoring',
            'description': 'Environmental monitoring functionality group'
        },
        {
            'name': 'Inventory Management',
            'description': 'Inventory management functionality group'
        }
    ]

    subgroups = [
        # Access Control subgroups
        {
            'name': 'Authentication',
            'description': 'Authentication subgroup',
            'group': 'Access Control'
        },
        {
            'name': 'NFC',
            'description': 'Near Field Communication subgroup',
            'group': 'Access Control'
        },
        {
            'name': 'Fingerprint',
            'description': 'Fingerprint subgroup',
            'group': 'Access Control'
        },
        {
            'name': 'Biometric',
            'description': 'Biometric subgroup',
            'group': 'Access Control'
        },

        # Safety Monitoring subgroups
        {
            'name': 'Fire Detection',
            'description': 'Fire detection subgroup',
            'group': 'Safety Monitoring'
        },
        {
            'name': 'Temperature Monitoring',
            'description': 'Temperature monitoring subgroup',
            'group': 'Safety Monitoring'
        },
        {
            'name': 'Camera Surveillance',
            'description': 'Camera surveillance subgroup',
            'group': 'Safety Monitoring'
        },
        {
            'name': 'Intrusion Detection',
            'description': 'Intrusion detection subgroup',
            'group': 'Safety Monitoring'
        },

        # Environmental Monitoring subgroups
        {
            'name': 'Humidity Monitoring',
            'description': 'Humidity monitoring subgroup',
            'group': 'Environmental Monitoring'
        },
        {
            'name': 'Air Quality Monitoring',
            'description': 'Air quality monitoring subgroup',
            'group': 'Environmental Monitoring'
        },
        {
            'name': 'Gas Detection',
            'description': 'Gas detection subgroup',
            'group': 'Environmental Monitoring'
        },
        {
            'name': 'Light Intensity Monitoring',
            'description': 'Light intensity monitoring subgroup',
            'group': 'Environmental Monitoring'
        },

        # Inventory Management subgroups
        {
            'name': 'Stock Level Monitoring',
            'description': 'Stock level monitoring subgroup',
            'group': 'Inventory Management'
        },
        {
            'name': 'RFID Tracking',
            'description': 'RFID tracking subgroup',
            'group': 'Inventory Management'
        },
        {
            'name': 'Barcode Scanning',
            'description': 'Barcode scanning subgroup',
            'group': 'Inventory Management'
        }
    ]

    for group_data in groups:
        group_name = group_data['name']
        group = DeviceGroup.objects(name=group_name).first()
        if not group:
            group = DeviceGroup(name=group_name, description=group_data['description'])
            group.save()

    for subgroup_data in subgroups:
        group_name = subgroup_data.pop('group')
        group = DeviceGroup.objects(name=group_name).first()
        if not group:
            continue  # Skip subgroup creation if the group doesn't exist
        subgroup_name = subgroup_data['name']
        subgroup = DeviceSubGroup.objects(name=subgroup_name, group=group).first()
        if not subgroup:
            subgroup_data['group'] = group
            subgroup = DeviceSubGroup(**subgroup_data)
            subgroup.save()
