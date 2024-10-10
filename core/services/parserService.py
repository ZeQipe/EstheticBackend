from services.encriptionService import Encriptions


class Separement:
    @staticmethod
    def packing_tags(tags: list) -> list:
        if not tags:
            return tags

        id_list = []
        while len(id_list) < len(tags):
            id = Encriptions.generate_string(8, False)
            if id not in id_list:
                id_list.append(Encriptions.generate_string(8, False))
            
        tag_response = []
        for i in range(len(id_list)):
            tag_dict = {"tagId" : id_list[i],
                        "label" : tags[i]}
            
            tag_response.append(tag_dict)
        
        return tag_response


    @staticmethod
    def unpacking_tags(tags: list[dict]) -> list[str]:
        print(tags, type(tags))
        if not tags:
            return []
        
        prew_tags = []
        for i in tags:
            prew_tags.append(i["label"])
        
        return prew_tags
    
