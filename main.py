import json
import os
import re
import requests
import time
import typer


def main(
    path: str = typer.Option(..., prompt=True),
    username: str = typer.Option(..., prompt=True),
    password: str = typer.Option(..., prompt=True, hide_input=True)
):
    # setting up workspace
    create_folder(path)
    os.chdir(path)
    print(f"Current working directory: {os.getcwd()}")
    working_directory = os.getcwd()

    token = authorize(username, password)
    projects = get_projects(token)
    for project in projects:
        project_uuid = project['uuid']
        project_name = project['name']
        project_artwork_url = project['artwork_url']
        project_user_sets = project['user_sets']
        
        if not os.path.exists(project_name):
            create_folder(project_name)

            # working in project directory
            os.chdir(project_name)
            
            # save project json
            save_project(project)

            # grab project artwork
            save_image(project_artwork_url)

            # save tags as empty files for ease of searching
            save_tags(project_user_sets)

            # process timeline
            process_timeline(project_uuid, token)

            # back to parent directory
            os.chdir(working_directory) 

def save_project(project):
    with open('project.json', 'w') as file:
        file.write(json.dumps(project))
        
def process_timeline(
    uuid: str,
    token: str
):
    working_directory = os.getcwd()

    # get timeline
    timeline = get_timeline(uuid, token)
    
    # save timeline json
    with open('timeline.json', 'w') as file:
        file.write(json.dumps(timeline))

    versions = timeline['versions']
    for version in versions:
        revision = version['uuid']
        stream_url = version['stream_url']
        version_no = str(version['version'])

        create_folder(version_no)
        os.chdir(version_no)
        print(f"Current working directory: {os.getcwd()}")

        # save stream url
        if stream_url:
            download_file(stream_url, "mp3")

        # save stems
        zip_url = get_zip_url(revision, token)
        if zip_url:
            download_file(zip_url, "zip")

        time.sleep(1)
        
        os.chdir(working_directory) 

def download_file(url, file_extension):
    # The link should be of the file directly
    r = requests.get(url)

    # If extension does not exist in end of url, append it
    if file_extension not in url.split("/")[-1]:
        filename = f'{url.split("/")[-1].split("?")[0]}{file_extension}'
    # Else take the last part of the url as filename
    else:
        filename = url.split("/")[-1].split("?")[0]

    with open(filename, 'wb') as f:
        # You will get the file in base64 as content
        f.write(r.content)

def get_zip_url(uuid, token):
    zip_url = None
    authorization = 'Bearer ' + token
    url = f"https://api.splice.com/studio/revisions/{uuid}/zip"
    print(url)
    payload = {}
    headers = {
        'Authorization': authorization,
        'Cookie': 'XSRF-TOKEN=S86-_Xg0-UQdAnSOVy_04h3oCa8:1678861567951; __cf_bm=KBrSwjeRUBxr3jgWUZVW9ZIhtoz3bfjcozu2bc.WLS8-1678861568-0-AcR8rZOAWodEn6jaT8B494CrqwvLF596p8cq2G8I6ZK+4QyuEVCL9nJHZlxQY9ydOzQmZqyhCa+8uak1dyGNLbEn48haoiq2lKgS5RwGajoD; _cfuvid=VBcPgTsPihe5j3.dmDsIqbroOajlaOHLyVPUHgEwiJk-1678608164618-0-604800000; _splice_web_session=TEpJR2d5YlNJSVYrYmFDcGxxUWVPTkVpQ2YrUXBPcTBRaE83dlNFYmNxS3o2ckpWMmhTTGRHZ0dDTVY2OUZ4SjZqMmJZemhwVVpnUW1Zc2FkZnMrOVdaUmREdGdWY2xRR29xMFYzSlprRkdGL1VrR1VtdG1pYmZKa3JsQUhGRmV1ZEUxclNzeGpZRmYvOFFlZ3ZJbnRXcjcycmh0NWhSU3VyVmhmY2RVUmFLRS9lMHJEL3ZSQzNtK2d6R2VRTGsxMVh6T2g1eGY4Njl4U2NnUUVQMmJ2TXhGbEY3YnFJemFTMENJck82K3NBaz0tLXZVakkyeWdmTXRSQk00REFtK3pOckE9PQ%3D%3D--ddbe7c13917f7d8e94f25d2e0ec426b249df9456'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    timeline = json.loads(response.text)
    if "zip_url" in timeline.keys():
        zip_url = timeline["zip_url"]
    return zip_url

def get_timeline(uuid, token):
    authorization = 'Bearer ' + token
    url = f"https://api.splice.com/studio/projects/{uuid}/timeline?start=0"
    print(url)

    payload = {}
    headers = {
        'Authorization': authorization,
        'Cookie': 'XSRF-TOKEN=S86-_Xg0-UQdAnSOVy_04h3oCa8:1678861567951; __cf_bm=KBrSwjeRUBxr3jgWUZVW9ZIhtoz3bfjcozu2bc.WLS8-1678861568-0-AcR8rZOAWodEn6jaT8B494CrqwvLF596p8cq2G8I6ZK+4QyuEVCL9nJHZlxQY9ydOzQmZqyhCa+8uak1dyGNLbEn48haoiq2lKgS5RwGajoD; _cfuvid=VBcPgTsPihe5j3.dmDsIqbroOajlaOHLyVPUHgEwiJk-1678608164618-0-604800000; _splice_web_session=TEpJR2d5YlNJSVYrYmFDcGxxUWVPTkVpQ2YrUXBPcTBRaE83dlNFYmNxS3o2ckpWMmhTTGRHZ0dDTVY2OUZ4SjZqMmJZemhwVVpnUW1Zc2FkZnMrOVdaUmREdGdWY2xRR29xMFYzSlprRkdGL1VrR1VtdG1pYmZKa3JsQUhGRmV1ZEUxclNzeGpZRmYvOFFlZ3ZJbnRXcjcycmh0NWhSU3VyVmhmY2RVUmFLRS9lMHJEL3ZSQzNtK2d6R2VRTGsxMVh6T2g1eGY4Njl4U2NnUUVQMmJ2TXhGbEY3YnFJemFTMENJck82K3NBaz0tLXZVakkyeWdmTXRSQk00REFtK3pOckE9PQ%3D%3D--ddbe7c13917f7d8e94f25d2e0ec426b249df9456'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    timeline = json.loads(response.text)
    return timeline

def save_tags(
    user_sets: list
):
    if user_sets:
        for user_set in user_sets:
            open(re.sub('[^\w_.)( -]', '', user_set['name']), 'a').close()

def save_image(
    image_url: str
):
    image_data = requests.get(image_url).content
    with open('image.jpg', 'wb') as handler:
        handler.write(image_data)


def create_folder(
    path: str
):
    if not os.path.isdir(path):
        print(f"Creating intermediate directories: {path}")
        os.makedirs(path)


def authorize(
    username: str,
    password: str
):
    url = "https://auth.splice.com/u/login?state=hKFo2SBmbERIY1lqMEhqUW1ydElDX3JGSXJ3N1BaYnk0QmFLeaFur3VuaXZlcnNhbC1sb2dpbqN0aWTZIDBWeFYwU21LcmtFYTBadW42bW42RmxDalRsUi1CTFpVo2NpZNkgSjVKVkNHa0ptdG9NNWVpSThMR2tQdW1hOTNleFFWOEg"
    payload = {
        'state': 'hKFo2SBmbERIY1lqMEhqUW1ydElDX3JGSXJ3N1BaYnk0QmFLeaFur3VuaXZlcnNhbC1sb2dpbqN0aWTZIDBWeFYwU21LcmtFYTBadW42bW42RmxDalRsUi1CTFpVo2NpZNkgSjVKVkNHa0ptdG9NNWVpSThMR2tQdW1hOTNleFFWOEg',
        'username': username,
        'password': password,
        'action': 'default'
    }
    files = [
    ]
    headers = {
        'Cookie': '__cf_bm=BVk4bSAkrG2MT_Z.AohYtCi3OgyFlB0.6eHwKBVvW.U-1678850155-0-AbUHS/MxMhQqLCTHradNgAmUNxv6J8TIrZJ1O/b9jR4lGpBKfwfueE/9yGrHYafQEMAnJvwrYWtUIiX/E3EPtfn1o0+BcCVkBEuG/xKcUJTT; _cfuvid=VBcPgTsPihe5j3.dmDsIqbroOajlaOHLyVPUHgEwiJk-1678608164618-0-604800000; _splice_web_session=TEpJR2d5YlNJSVYrYmFDcGxxUWVPTkVpQ2YrUXBPcTBRaE83dlNFYmNxS3o2ckpWMmhTTGRHZ0dDTVY2OUZ4SjZqMmJZemhwVVpnUW1Zc2FkZnMrOVdaUmREdGdWY2xRR29xMFYzSlprRkdGL1VrR1VtdG1pYmZKa3JsQUhGRmV1ZEUxclNzeGpZRmYvOFFlZ3ZJbnRXcjcycmh0NWhSU3VyVmhmY2RVUmFLRS9lMHJEL3ZSQzNtK2d6R2VRTGsxMVh6T2g1eGY4Njl4U2NnUUVQMmJ2TXhGbEY3YnFJemFTMENJck82K3NBaz0tLXZVakkyeWdmTXRSQk00REFtK3pOckE9PQ%3D%3D--ddbe7c13917f7d8e94f25d2e0ec426b249df9456; did=s%3Av0%3Ab3305c60-c2df-11ed-b588-77004c3d338f.oOA7YhwSX5MPAbuE1HrJjreOg1KiLKq%2BG82NryM%2BVMw; did_compat=s%3Av0%3Ab3305c60-c2df-11ed-b588-77004c3d338f.oOA7YhwSX5MPAbuE1HrJjreOg1KiLKq%2BG82NryM%2BVMw'
    }
    response = requests.request(
        "POST", url, headers=headers, data=payload, files=files)

    token = response.cookies['CF_Authorization']
    print(f"Token: {token}")
    return token


def get_projects(
    token: str
):
    authorization = 'Bearer ' + token
    url = "https://api.splice.com/studio/projects?collaborator=&f=&page=1&per_page=300&q=&set=&version=2"
    payload = {}
    headers = {
        'Authorization': authorization,
        'Cookie': 'XSRF-TOKEN=S86-_Xg0-UQdAnSOVy_04h3oCa8:1678861567951; __cf_bm=KBrSwjeRUBxr3jgWUZVW9ZIhtoz3bfjcozu2bc.WLS8-1678861568-0-AcR8rZOAWodEn6jaT8B494CrqwvLF596p8cq2G8I6ZK+4QyuEVCL9nJHZlxQY9ydOzQmZqyhCa+8uak1dyGNLbEn48haoiq2lKgS5RwGajoD; _cfuvid=VBcPgTsPihe5j3.dmDsIqbroOajlaOHLyVPUHgEwiJk-1678608164618-0-604800000; _splice_web_session=TEpJR2d5YlNJSVYrYmFDcGxxUWVPTkVpQ2YrUXBPcTBRaE83dlNFYmNxS3o2ckpWMmhTTGRHZ0dDTVY2OUZ4SjZqMmJZemhwVVpnUW1Zc2FkZnMrOVdaUmREdGdWY2xRR29xMFYzSlprRkdGL1VrR1VtdG1pYmZKa3JsQUhGRmV1ZEUxclNzeGpZRmYvOFFlZ3ZJbnRXcjcycmh0NWhSU3VyVmhmY2RVUmFLRS9lMHJEL3ZSQzNtK2d6R2VRTGsxMVh6T2g1eGY4Njl4U2NnUUVQMmJ2TXhGbEY3YnFJemFTMENJck82K3NBaz0tLXZVakkyeWdmTXRSQk00REFtK3pOckE9PQ%3D%3D--ddbe7c13917f7d8e94f25d2e0ec426b249df9456'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    projects = json.loads(response.text)["projects"]

    return (projects)


if __name__ == "__main__":
    typer.run(main)
