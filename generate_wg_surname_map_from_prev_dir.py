import os

def generate_configuration_files(root_dir, output_dir):
    if not os.path.exists(root_dir):
        print(f"Directory not found: {root_dir}")
        return
    else:
        print(f"Directory found: {root_dir}")

    working_groups = []
    surnames_to_wg = []

    # Traverse the first level (AG groups)
    for ag in os.listdir(root_dir):
        ag_path = os.path.join(root_dir, ag)
        if os.path.isdir(ag_path) and ag.startswith('AG_'):
            working_groups.append(ag)

            # Traverse the second level (Surnames)
            for member in os.listdir(ag_path):
                member_path = os.path.join(ag_path, member)
                if os.path.isdir(member_path):  # Ensure it's a directory
                    surnames_to_wg.append(f"{member},{ag}")

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Path for the working groups file
    working_groups_path = os.path.join(output_dir, 'working_groups.txt')
    # Path for the surnames to working group mappings file
    surnames_to_wg_path = os.path.join(output_dir, 'surnames_to_wg.txt')

    with open(working_groups_path, 'w') as wg_file:
        for wg in sorted(working_groups):
            wg_file.write(wg + '\n')

    with open(surnames_to_wg_path, 'w') as stw_file:
        for line in sorted(surnames_to_wg):
            stw_file.write(line + '\n')

    print("Configuration files generated successfully at:", output_dir)

# Example usage
root_directory = r'V:\Martina\LMU-Server'  # Adjust accordingly
output_directory = 'C:\\desired\\output\\path'  # Specify your desired output directory
generate_configuration_files(root_directory, output_directory)