import os, traceback, json, configparser, boto3

client = boto3.client('ssm')
env = 'dev'
app_config_path = 'parameterStore'
full_config_path = '/' + env + '/' + app_config_path
# Initialize app at global scope for reuse across invocations
app = None


def __init__(self, config):
    """
    Construct new MyApp with configuration
    :param config: application configuration
    """
    self.config = config


def get_config(self):
    return self.config

def load_config(ssm_parameter_path):
    """
    Load configparser from config stored in SSM Parameter Store
    :param ssm_parameter_path: Path to app config in SSM Parameter Store
    :return: ConfigParser holding loaded config
    """
    configuration = configparser.ConfigParser()
    try:
        # Get all parameters for this app
        param_details = client.get_parameters_by_path(
            Path=ssm_parameter_path,
            Recursive=False,
            WithDecryption=True
        )

        # Loop through the returned parameters and populate the ConfigParser
        if 'Parameters' in param_details and len(param_details.get('Parameters')) > 0:
            for param in param_details.get('Parameters'):
                param_path_array = param.get('Name').split("/")
                section_position = len(param_path_array) - 1
                section_name = param_path_array[section_position]
                config_values = json.loads(param.get('Value'))
                config_dict = {section_name: config_values}
                print("Found configuration: " + str(config_dict))
                configuration.read_dict(config_dict)

    except:
        print("Encountered an error loading config from SSM.")
        traceback.print_exc()
    finally:
        return configuration


if app is None:
        print("Loading config and creating new MyApp...")
        config = load_config(full_config_path)
        app = MyApp(config)

print "MyApp config is " + str(app.get_config()._sections)