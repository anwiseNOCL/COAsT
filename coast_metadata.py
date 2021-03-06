def get_package(package_path="package.json"):
    from types import SimpleNamespace
    import json

    with open(package_path, "r") as package_file:
        package = json.load(package_file)
    return SimpleNamespace(**package)


def represent_ordered_dict(dumper, data):
    import yaml

    value = []

    for item_key, item_value in data.items():
        node_key = dumper.represent_data(item_key)
        node_value = dumper.represent_data(item_value)

        value.append((node_key, node_value))

    return yaml.nodes.MappingNode(u'tag:yaml.org,2002:map', value)


def generate_conda(directory="conda"):
    import yaml
    from os import path
    from collections import OrderedDict

    yaml.add_representer(OrderedDict, represent_ordered_dict)

    package = get_package()
    package_metadata = OrderedDict({
        "package": {
            "name": package.name.lower(),
            "version": package.version
        },
        "source": {
            "url": f"https://pypi.io/packages/source/{package.name[0]}/{package.name}/{package.name}-{package.version}.tar.gz"
        },
        "build": {
            "number": 0,
            "script": "pip install https://files.pythonhosted.org/packages/83/cc/c62100906d30f95d46451c15eb407da7db201e30f42008f3643945910373/graphviz-0.14-py2.py3-none-any.whl"  # TODO: I don't understand what this is for? Why are we linking to a specific file like this??? (matcaz)
        },
        "requirements": {
            "host": package.install_requires,
            "run": package.install_requires
        },
        # TODO --------------------
        "test": {
            "imports": [
                "coast"
            ]
        },
        # TODO --------------------
        "about": {
            "home": package.url,
            "license": package.license,
            "license_family": package.license_family,
            "summary": package.description,
        },
        # "extra": {
        #     "recipe-maintainers": [
        #         package.github
        #     ]
        # }
    })

    yaml_path = path.join(directory, "meta.yaml")
    with open(yaml_path, "w") as meta_file:
        yaml.dump(package_metadata, meta_file)


if __name__ == "__main__":
    generate_conda()
