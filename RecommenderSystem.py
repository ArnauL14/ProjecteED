import json
import math
import os

class RecommenderSystem:
    def __init__(self, vectors_path, image_data=None, image_id=None):
        self.image_data = image_data
        self.image_id = image_id
        self.vectors_json = {}
        self.uuid_to_vector = {}

        if os.path.exists(vectors_path):
            with open(vectors_path, 'r') as f:
                self.vectors_json = json.load(f).get("vectors", {})

    def cosine_similarity(self, vec1, vec2):
        dot = sum(a * b for a, b in zip(vec1, vec2))
        norm_a = math.sqrt(sum(a * a for a in vec1))
        norm_b = math.sqrt(sum(b * b for b in vec2))
        return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0

    def preprocess(self):
        if not self.image_id: return
        # [cite_start]El JSON usa filenames sense extensió com a claus [cite: 907]
        for filename_no_ext, embeddings in self.vectors_json.items():
            # Reconstruïm el nom que ha guardat ImageFiles
            filename = filename_no_ext + ".png"
            uuid = self.image_id.get_uuid(filename)
            if uuid:
                self.uuid_to_vector[uuid] = embeddings.get("image_embedding")

    def find_similar_images(self, query_uuid, k=10):
        query_vec = self.uuid_to_vector.get(query_uuid)
        if not query_vec:
            class G:
                def __init__(self): self.images = []
            return G()

        results = []
        for uuid, vec in self.uuid_to_vector.items():
            if uuid == query_uuid: continue
            results.append((uuid, self.cosine_similarity(query_vec, vec)))
        
        results.sort(key=lambda x: x[1], reverse=True)
        top_k = [r[0] for r in results[:k]]
        
        class GalleryObj:
            def __init__(self, imgs): self.images = imgs
        return GalleryObj(top_k)

    def find_transition_prompts(self, uuid1, uuid2):
        return []
