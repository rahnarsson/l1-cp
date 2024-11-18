import os
import yaml
from jinja2 import Environment, FileSystemLoader

# Paths to templates and output files
TEMPLATE_DIR = "./templates"
INSTALL_CONFIG_TEMPLATE = "install-config.j2"
AGENT_CONFIG_TEMPLATE = "agent-config.j2"
OPENSHIFT_GITOPS_TEMPLATE = "01_openshift-gitops.j2"
OPENSHIFT_CS_TEMPLATE = "catalogsource.j2"

# Output directories
WORKING_DIR = "./workingdir"
OPENSHIFT_DIR = os.path.join(WORKING_DIR, "openshift")

INSTALL_CONFIG_OUTPUT = os.path.join(WORKING_DIR, "install-config.yaml")
AGENT_CONFIG_OUTPUT = os.path.join(WORKING_DIR, "agent-config.yaml")
OPENSHIFT_GITOPS_OUTPUT = os.path.join(OPENSHIFT_DIR, "01_openshift-gitops-operator.yaml")
OPENSHIFT_CS_OUTPUT = os.path.join(OPENSHIFT_DIR, "02_catalogsource.yaml")

# Function to load YAML input file
def load_input_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Function to render a Jinja2 template
def render_template(template_file, context):
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template(template_file)
    return template.render(context)

# Function to ensure directories exist
def ensure_directories():
    os.makedirs(WORKING_DIR, exist_ok=True)
    os.makedirs(OPENSHIFT_DIR, exist_ok=True)

# Main program
def main():
    # Ensure output directories exist
    ensure_directories()

    # Path to the input configuration file
    input_config_path = "input-config.yaml"
    
    # Load the input configuration
    input_config = load_input_config(input_config_path)
    
    # Generate install-config.yaml in WORKING_DIR
    install_config_content = render_template(INSTALL_CONFIG_TEMPLATE, input_config)
    with open(INSTALL_CONFIG_OUTPUT, 'w') as install_file:
        install_file.write(install_config_content)
    print(f"{INSTALL_CONFIG_OUTPUT} generated successfully.")
    
    # Generate agent-config.yaml in WORKING_DIR/openshift
    agent_config_content = render_template(AGENT_CONFIG_TEMPLATE, input_config)
    with open(AGENT_CONFIG_OUTPUT, 'w') as agent_file:
        agent_file.write(agent_config_content)
    print(f"{AGENT_CONFIG_OUTPUT} generated successfully.")

    # Generate 01_openshift-gitops-operator.yaml in WORKING_DIR/openshift
    openshift_gitops_content = render_template(OPENSHIFT_GITOPS_TEMPLATE, input_config)
    with open(OPENSHIFT_GITOPS_OUTPUT, 'w') as agent_file:
        agent_file.write(openshift_gitops_content)
    print(f"{OPENSHIFT_GITOPS_OUTPUT} generated successfully.")

    # Generate 02_catalogsource.yaml in WORKING_DIR/openshift
    openshift_cs_content = render_template(OPENSHIFT_CS_TEMPLATE, input_config)
    with open(OPENSHIFT_CS_OUTPUT, 'w') as agent_file:
        agent_file.write(openshift_cs_content)
    print(f"{OPENSHIFT_CS_OUTPUT} generated successfully.")

if __name__ == "__main__":
    main()