import re
import os


def _extract_pipeline_order(current_directory):
    """
    Extracts the PIPELINE_ORDER list from the content of the main file.

    :param current_directory: The content of the main file.
    :return: The extracted PIPELINE_ORDER list or None if not found.
    """
    main_path = os.path.join(current_directory, 'main.py')
    with open(main_path, 'r') as file:
        return file.read()
    main_content = _read_main_file_content(main_path)
    pipeline_order_match = re.search(r'PIPELINE_ORDER\s*=\s*\[([^\]]+)\]', main_content)
    if pipeline_order_match:
        return pipeline_order_match.group(1).replace("'", "").replace('"', "").split(',')
    return None
