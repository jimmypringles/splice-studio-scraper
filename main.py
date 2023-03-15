import json
import os
import requests
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
    
    token = authorize(username, password)
    projects = get_projects(token)
    for project in projects:
        project_uuid = project['uuid']
        project_name = project['name']
        
        create_folder(project_name)
        os.chdir(project_name) # working in project directory
        
        print(os.path.dirname('project.json'))
        with open('project.json', 'w') as file:
            file.write(json.dumps(project))
        
        os.chdir(path) # back to parent directory
        

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
