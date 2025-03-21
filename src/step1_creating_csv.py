import os
import yaml
import csv
import logging
from step0_utility_functions import Utility


class MetadataExtraction:

    def __init__(self):
        pass

    def extract_slakh_metadata(self, root_dir, output_csv):
        """
        Extracts metadata from all YAML files in the Slakh2100 dataset directory and writes to a CSV file.

        Args:
        root_dir (str): Path to the root directory of the Slakh2100 dataset.
        output_csv (str): Path to the output CSV file.
        """
        try:
            logger.info('Creating a csv file to store metadata in structured format.')
            # Open the CSV file for writing
            with open(output_csv, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                # Write header row
                writer.writerow([
                    'Folder Name', 'UUID', 'Track Name', 'Instrument Class',
                    'MIDI Program Name', 'Integrated Loudness', 'Is Drum',
                    'Plugin Name', 'Program Number'
                ])

                # Traverse the dataset directory
                for folder in os.listdir(root_dir):
                    folder_path = os.path.join(root_dir, folder)
                    if os.path.isdir(folder_path):
                        # Check for the YAML file in the folder
                        yaml_file_path = os.path.join(folder_path, 'metadata.yaml')
                        if os.path.exists(yaml_file_path):
                            # Process the YAML file
                            with open(yaml_file_path, 'r') as file:
                                try:
                                    data = yaml.safe_load(file)
                                    
                                    # Extract folder name and UUID
                                    uuid = data.get('UUID', 'Unknown')
                                    stems = data.get('stems', {})

                                    # Extract information for each stem (track)
                                    for track_name, track_info in stems.items():
                                        writer.writerow([
                                            folder,  # Folder name
                                            uuid,  # UUID
                                            track_name + ".flac",  # Track name (e.g., S00, S01)
                                            track_info.get('inst_class', 'Unknown'),  # Instrument class
                                            track_info.get('midi_program_name', 'Unknown'),  # MIDI program name
                                            track_info.get('integrated_loudness', 'Unknown'),  # Integrated loudness
                                            track_info.get('is_drum', 'Unknown'),  # Is drum
                                            track_info.get('plugin_name', 'Unknown'),  # Plugin name
                                            track_info.get('program_num', 'Unknown')  # Program number
                                        ])
                                    logger.info('Metadata fetched from multiple metadata yaml files and stored in one csv file.')

                                except yaml.YAMLError as e:
                                    print(f"Error reading YAML file: {yaml_file_path}, Error: {e}")
                                    raise e
                                
        except Exception as e:
            print(f"Error: {e}")


# Example usage
if __name__ == "__main__":

    # SETTING UP THE LOGGING MECHANISM
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    Utility().create_folder('Logs')
    params = Utility().read_params()

    main_log_folderpath = params['Logs']['Logs_Folder']
    data_restructuring_processing_logfile_path = params['Logs']['Data_Restructuring_Processing']

    file_handler = logging.FileHandler(os.path.join(
        main_log_folderpath, data_restructuring_processing_logfile_path))
    formatter = logging.Formatter(
        '%(asctime)s : %(levelname)s : %(filename)s : %(message)s')

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # STARTING THE EXECUTION OF FUNCTIONS

    # Type of data
    data = 'train'
    
    # Root directory of Slakh2100 dataset
    slakh_root_dir = os.path.join('Slakh2100', data)

    # Output CSV file path
    output_csv_path = f'slakh2100_metadata_{data}.csv'

    # Extract metadata and write to CSV
    me = MetadataExtraction()
    me.extract_slakh_metadata(slakh_root_dir, output_csv_path)

