import os

def get_pdf_blob(file):
    with open(file, 'rb') as pdf_file:
        blob_data = pdf_file.read()
    return blob_data

def find_files(filename):
    """
    Function which will find wkhtmltopdf executable file
    """
    root_directory = os.getcwd()
    for root, dirs, files in os.walk(root_directory):
        if filename in files:
            return os.path.join(root, filename)
    return None

def get_db_columns(report_folder):
    try:
        with open(report_folder + "//" + '01-robots.txt', 'r') as robots_file:
            robots_content = robots_file.read()
    except:
        robots_content = 0
        pass
    try:
        with open(report_folder + "//" + '02-sitemap.txt', 'r') as sitemap_xml:
            sitemap_content = sitemap_xml.read()
    except:
        sitemap_content = 0
        pass
    try:
        with open(report_folder + "//" + '03-sitemap_links.txt', 'r') as sitemap_links:
            sitemap_links_content = sitemap_links.read()
    except:
        sitemap_links_content = 0
        pass
    try:
        with open(report_folder + "//" + '04-dorking_results.txt', 'r') as dorking_file:
            dorking_content = dorking_file.read()
    except:
        dorking_content = 0
        pass
    return robots_content, sitemap_content, sitemap_links_content, dorking_content
