import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():
    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):
                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    # Initialising the joint probability variable.
    prob_joint = 1

    # Iterating and calculating conditional probability of each individual.
    for person in people:
        # Storing names of parents.
        mother = people[person]['mother']
        father = people[person]['father']

        # The 'trait' boolean is for whether the person has the trait.
        trait = person in have_trait

        # Stores the number of gene copies of the individual.
        copies = (
            1 if person in one_gene else
            2 if person in two_genes else
            0
        )

        # If no parents then an independent event occurs.
        # Hence, an unconditional probability with preset values is used.
        if not mother or not father:
            prob_gene = PROBS["gene"][copies]

        # Otherwise, conditional probability is used for child.
        else:
            # Probabilities of parents passing on genes.
            prob_father = prob_inheritance(father, one_gene, two_genes)
            prob_mother = prob_inheritance(mother, one_gene, two_genes)

            # Calculating joint gene probability of child.
            if copies == 2:
                prob_gene = prob_father * prob_mother
            elif copies == 1:
                # Probability of (F and not M) or (not F and M).
                prob_gene = (prob_father * (1 - prob_mother) +
                             (1 - prob_father) * prob_mother)
            else:
                prob_gene = (1 - prob_father) * (1 - prob_mother)

        # Storing probability of possessing the trait.
        prob_trait = PROBS["trait"][copies][trait]

        # Multiplying joint probability with that of gene and trait.
        prob_joint *= prob_gene * prob_trait

    return prob_joint


# Calculates inherit probability based on parent gene copies.
def prob_inheritance(parent, one_gene, two_genes):
    if parent in two_genes:
        return 1 - PROBS["mutation"]
    elif parent in one_gene:
        return 0.5
    else:
        return PROBS["mutation"]


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        # Storing number of gene copies.
        copies = (
            1 if person in one_gene else
            2 if person in two_genes else
            0
        )

        # Checking whether trait is possessed.
        trait = person in have_trait

        # Adding stored values to respective indices in dictionary.
        probabilities[person]["gene"][copies] += p
        probabilities[person]["trait"][trait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    # Iterating and normalising probability of each individual.
    for person in probabilities:
        # Storing the gene and trait probabilities in 2 separate dictionaries.
        genes = probabilities[person]["gene"]
        traits = probabilities[person]["trait"]

        # Finding scale factors using Bayes' rule and conditional probability.
        gene_factor = 1 / sum(genes.values())
        trait_factor = 1 / sum(traits.values())

        # Updating dictionary by multiplying probabilities with scale factors.
        probabilities[person]["gene"] = (
            {gene: prob * gene_factor for gene, prob in genes.items()}
        )

        probabilities[person]["trait"] = (
            {trait: prob * trait_factor for trait, prob in traits.items()}
        )


if __name__ == "__main__":
    main()
