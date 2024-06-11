import os
import urllib.request
import json

try:
    KEY = os.environ["ARTDATA_KEY"]
except:  # noqa
    with open("artdata.env") as f:
        KEY = f.read().split("=")[-1]

print(KEY)

hdr = {
    "Content-Type": "application/json",
    "Cache-Control": "no-cache",
    "Ocp-Apim-Subscription-Key": KEY,
}


def get_definitions():
    v = {}
    try:
        url = "https://api.artdatabanken.se/taxonlistservice/v1/definitions"

        hdr = {
            # Request headers
            "Cache-Control": "no-cache",
            "Ocp-Apim-Subscription-Key": KEY,
        }

        req = urllib.request.Request(url, headers=hdr)

        req.get_method = lambda: "GET"
        response = urllib.request.urlopen(req)
        print(response.getcode())
        v = json.loads(response.read())
    except Exception as e:
        print(e)

    return v


def all_lists(v):
    res = []
    for item in v["conservationLists"]:
        res.append(item["id"])

    return res


def species_list(sp):
    res = []
    for taxa_list in sp["natureConservationListTaxa"]:
        for taxa in taxa_list["taxonInformation"]:
            res += taxa.values()

    return res


def save_tmp(v, name="tmp.json"):
    with open(name, "w") as f:
        f.write(json.dumps(v, indent=4))


def get_species(lists=[1, 8], fields=["scientificname", "swedishname"]):
    v = {}
    try:
        url = "https://api.artdatabanken.se/taxonlistservice/v1/taxa"
        # Request body
        data = {
            "conservationListIds": lists,
            "outputFields": fields,
        }
        data = json.dumps(data)
        req = urllib.request.Request(url, headers=hdr, data=bytes(data.encode("utf-8")))

        req.get_method = lambda: "POST"
        response = urllib.request.urlopen(req)
        print(response.getcode())
        v = json.loads(response.read())
    except Exception as e:
        print(e)

    return v


if __name__ == "__main__":
    print("Getting definitions...")
    defs = get_definitions()

    list_ids = all_lists(defs)
    print(f"fetching {len(list_ids)} lists")
    sp = get_species(lists=list_ids, fields=["swedishname"])
    all_species = list(set(species_list(sp)))
    print(f"{len(all_species)} total species")

    print("fetching list of species to remove")
    remove_species = list(
        set(
            species_list(
                get_species(lists=[247, 234, 262, 264], fields=["swedishname"])
            )
        )
    )
    print(f"{len(remove_species)} species to remove")
    final = []
    for sp in all_species:
        if sp not in remove_species:
            final.append(sp)
        else:
            print(f"Removing {sp}")
    print(f"final length: {len(final)}")
    with open("result.json", "w") as f:
        f.write(json.dumps({"species": final}))
