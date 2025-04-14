from mdutils.mdutils import MdUtils
from urllib.parse import urlparse
import json
import sys
import os

def single_API_doc(single_req,md):
    global API_COUNTER
    API_COUNTER += 1
    if not isinstance(single_req, dict):
        sys.exit("Function single_API_doc is not receiving a single request.")
    # API Name:
    api_name = single_req.get("name","")
    md.new_header(level = 3, title = f"{api_name}")
    md.new_paragraph(f"**Name**: {api_name}")
    # Method:
    api_method = (single_req.get("method",""))
    md.new_paragraph(f"**Method**: {api_method}")
    # Api URL:
    api_url = single_req.get("endpoint","")
    md.new_paragraph(f"**URL**: {api_url}")
    # API Endpoint:
    api_endpt = urlparse(single_req.get("endpoint","")).path
    md.new_paragraph(f"**Endpoint**: {api_endpt}")
    md.new_paragraph("**Request Description**: ")

    # [x]: Content-type
    # API content-type
    api_bd_content_type = single_req.get("body",{}).get("contentType","")
    md.new_paragraph(f"**Content-Type**: {api_bd_content_type}")

    # [x]:  Request body
    md.new_paragraph(r"**Request Body Parameters**:")
    req_body_params_eg_list = ["Field Name", "Required", "Data Type", "Example", "Remarks"]
    req_body_params_arr = single_req.get("body",{}).get("body",[])
    if isinstance(req_body_params_arr,list) and len(req_body_params_arr) > 0:
        for param in req_body_params_arr:
            req_body_params_eg_list.append(param.get("key",""))
            req_body_params_eg_list.append("")
            req_body_params_eg_list.append("")
            req_body_params_eg_list.append(param.get("value",""))
            req_body_params_eg_list.append("")
        md.new_table(columns= 5, rows = int(len(req_body_params_eg_list)/5), text = req_body_params_eg_list, text_align='left')
    else:
        md.new_paragraph("No Request Body Parameters", bold_italics_code='i', align = "center")

    # [x]: headers
    md.new_paragraph("**Headers**:")
    req_headers = ['\tAuthorization : Bearer (Token obtained from login)']
    if not len(single_req.get("headers", [])) == 0:
        for header in single_req["headers"]:
            req_headers.append(f"\t{header.get("key","")} : {header.get("value","")}")
    md.new_list(req_headers, marked_with='1')

    # [x]: Query Parameters - 
    md.new_paragraph("**Query Parameters**:")
    query_params_eg_list = ["Field Name", "Required", "Data Type", "Example", "Remarks"]
    if isinstance(single_req["params"],list) and len(single_req["params"]) > 0:
        for param in single_req.get("params",[]):
            query_params_eg_list.append(param["key"])
            query_params_eg_list.append("")
            query_params_eg_list.append("")
            query_params_eg_list.append(param["value"])
            query_params_eg_list.append("")
        md.new_table(columns= 5, rows = int(len(query_params_eg_list)/5), text = query_params_eg_list, text_align='left')
    else:
        # [x]: Print no query parameters if no such query parameters exist
        md.new_paragraph("No Query Parameters", bold_italics_code='i', align = "center")

    # [x]: Expected Response
    md.new_paragraph("**Expected Response:**")
    md.insert_code("", language='json')
    md.new_line(r"\newpage")

def create_markdown_API(node_req, md_fp, main_folder_name):

    # [x]2 : First create API docs from requests which are outside sub folders
    if len(node_req.get("requests",[])) > 0:
        folder_name = node_req.get("name")

        if not (folder_name == main_folder_name):
            md_fp.new_header(level = 2, title = folder_name)
        for req in node_req.get("requests",[]):
            single_API_doc(req,md_fp)

    # [x]3: Recurse into child folders
    if len(node_req.get("folders",[])) > 0:
        for child_dict in node_req.get("folders",[]):
            create_markdown_API(child_dict,md_fp,main_folder_name)

def create_API_doc(json_file, base_path, md_fpointer, main_fname):
    file_path = os.path.join(base_path,json_file)
    with open(file_path, encoding='utf-8') as fp_json:
        data = json.load(fp_json)
    return create_markdown_API(data, md_fpointer, main_fname)


if __name__ == '__main__':
    files_dir = r"D:\Parking App All APIs json"
    files = ["ParkingApp Admin.json",
                "Parking App & Website.json",
                "Parking App.json"
                ]
    API_COUNTER = 0
    # [x]1: First create the markdown file
    md_pointer = MdUtils(file_name = "Smart Parking API documentation", title ="Smart Parking API Documentation")
    for file in files:
        main_file_name = file.split(".")[0]
        md_pointer.new_header(level = 1, title = file.split(".")[0])
        create_API_doc(file,files_dir, md_pointer, main_file_name)
    
    # [x]4: Add table of contents and save the file:
    # Table of content auto-generated with level of heading = 2
    md_pointer.new_table_of_contents(table_title = 'Table of Contents', depth = 3)
    md_pointer.new_line(r"\newpage")
    # Create the markdown file - end of file creation
    md_pointer.create_md_file()
    print(f"Total API docs created {API_COUNTER}")