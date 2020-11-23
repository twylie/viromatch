import yaml


class Taxonomy():

    def __init__(self, tax_id):

        self.taxonomy = dict()
        self.lineage = None

        with open(tax_id, 'r') as tax_id_fh:
            for line in tax_id_fh:
                line = line.strip()
                taxid, name, parent, rank = line.split('\t')
                self.taxonomy.update({
                    taxid: {
                        'name': name,
                        'parent': parent,
                        'rank': rank
                    }
                })

        return

    def lookup_lineage(self, tax_id):

        lineage = dict()
        rank_i = 0

        if tax_id in self.taxonomy:
            rank = self.taxonomy[tax_id]['rank']
            name = self.taxonomy[tax_id]['name']
            parent = self.taxonomy[tax_id]['parent']
            rank_i += 1
            lineage.update({rank_i: {'rank': rank, 'name': name, 'parent': parent}})
            recursive_parent = parent
            while recursive_parent != '1':
                rank = self.taxonomy[recursive_parent]['rank']
                name = self.taxonomy[recursive_parent]['name']
                recursive_parent = self.taxonomy[recursive_parent]['parent']
                rank_i += 1
                lineage.update({rank_i: {'rank': rank, 'name': name, 'parent': recursive_parent}})
        else:
            lineage.update({1: {'rank': 'Unknown', 'name': 'Unknown', 'parent': 'Unknown'}})

        self.lineage = lineage

        return self

    def flatten_lineage(self):

        lineage_fields = list()
        if not self.lineage:
            return None
        else:
            for key in sorted(self.lineage):
                lineage_fields.append(self.lineage[key]['name'])
            lineage_fields.reverse()
            return ' --> '.join(lineage_fields)

    def superkingdom(self):

        superkingdom = None

        for level in sorted(self.lineage):
            if self.lineage[level]['rank'] == 'superkingdom':
                superkingdom = self.lineage[level]['name']

        if superkingdom is None:
            superkingdom = 'Unknown'

        return superkingdom

    def species(self):

        species = None

        for level in sorted(self.lineage):
            if self.lineage[level]['rank'] == 'species':
                species = self.lineage[level]['name']

        if species is None:
            species = 'unknown species'

        return species

    def genus(self):

        genus = None
        species = None

        for level in sorted(self.lineage):
            if self.lineage[level]['rank'] == 'genus':
                genus = self.lineage[level]['name']
            elif self.lineage[level]['rank'] == 'species':
                species = self.lineage[level]['name']

        if species is None:
            species = 'unknown species'

        if genus is None:
            genus = ' '.join(['unknown genus', '|', species])

        return genus

    def lineage_yaml(self):

        print(yaml.dump(self.lineage).strip())

        return


# __END__
