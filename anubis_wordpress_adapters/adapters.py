# from exceptions import ProductCreateException
import requests
from anubis_core.features.blog.models import CorePost
from anubis_core.features.blog.ports import IPostAdapter

class WordpressPostAdapter:
    def __init__(self, wordpress_api_url: str, access_token: str):
        self.wordpress_api_url = wordpress_api_url.rstrip('/') + "/wp/v2/posts"
        self.access_token = access_token
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def pull_post(self, id_product: int) -> CorePost:
        """Obtiene un post de WordPress por su ID."""
        print ("PULL POST")
        return ""
        response = requests.get(f"{self.wordpress_api_url}/{id_product}", headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return CorePost(
                post_id=data["id"],
                title=data["title"]["rendered"],
                content=data["content"]["rendered"],
                status=data["status"],
                link=data["link"]
            )
        else:
            raise Exception(f"Error al obtener post: {response.text}")

    def push_post(self, product: CorePost) -> CorePost:
        """Crea o actualiza un post en WordPress."""
        print ("PUSH POST")
        return ""
        data = {
            "title": product.title,
            "content": product.content,
            "status": product.status
        }
        if product.post_id:  # Si tiene ID, actualizar post existente
            url = f"{self.wordpress_api_url}/{product.post_id}"
            response = requests.post(url, json=data, headers=self.headers)
        else:  # Si no tiene ID, crear nuevo post
            response = requests.post(self.wordpress_api_url, json=data, headers=self.headers)
        
        if response.status_code in [200, 201]:
            data = response.json()
            return CorePost(
                post_id=data["id"],
                title=data["title"]["rendered"],
                content=data["content"]["rendered"],
                status=data["status"],
                link=data["link"]
            )
        else:
            raise Exception(f"Error al publicar post: {response.text}")

    def search_posts(self, search_text: str) -> list[CorePost]:
        """Busca posts en WordPress que coincidan con el texto dado."""
        response = requests.get(f"{self.wordpress_api_url}?search={search_text}", headers=self.headers)
        if response.status_code == 200:
            posts = response.json()
            return [
                CorePost(
                    post_id=post["id"],
                    title=post["title"]["rendered"],
                    content=post["content"]["rendered"],
                    status=post["status"],
                    link=post["link"]
                ) for post in posts
            ]
        else:
            raise Exception(f"Error al buscar posts: {response.text}")

