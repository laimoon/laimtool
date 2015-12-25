from pylxd import api


class LaimLaim(object):
    SOURCE_TYPE = (
        'image',
        'migration',
        'copy',
        'none',
    )

    def __init__(self):
        self.lxd = api.API()

    def envs(self):
        containers = self.lxd.list_containers()
        return containers

    def startenv(self, name, source_type, source_alias,
                 profiles, conf, ephemeral=False):

        container = self.lxd.container_init(
            {
                'name': name,
                'architecture': 2,
                'profiles': profiles,
                'ephemeral': ephemeral,
                'source': {
                    'type': source_type,
                    'alias': source_alias
                }
            }
        )

        return container
