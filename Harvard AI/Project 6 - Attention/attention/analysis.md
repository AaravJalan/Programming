# Analysis

## Layer 8, Head 7
> Checking for Adjectives

An adjective is a word that modifies a noun.

**Explanation:** In this attention head, adjectives appear to be paying attention to the nouns they modify.

To determine that this attention head had a relation between adjectives & nouns:
- I entered Sentence 1 and found four attention heads: 
  - Layer 8 Head 7
  - Layer 11 Head 11
  - Layer 10 Head 9
  - Layer 11 Head 9
  

- Then, to eliminate some options, I entered Sentence 2. This left me with:
  - Layer 8 Head 7
  - Layer 11 Head 11


- I came to a final conclusion by entering Sentence 3, which eliminated Layer 11, Head 11.

I realised that there was a clear relationship between the adjective & the noun in this head, 
as there was a distinct bright white cell at the intersecting column between [MASK] and the noun, 
while the remaining cells were either grey or black.

### Example Sentences:
1. The [MASK] cat spilled water everywhere.
2. The cat climbed the tall, [MASK] tree.
3. The naughty, [MASK] cat ran away from the dog.

## Layer 5, Head 12

> Checking for Determiners

A determiner is a word that directly modifies the noun after it.
This attention head clearly showcased a successive relationship - the intersection between the noun and [MASK] was always the brightest white/grey cell. 
The rest of the cells were either dark grey or black.
I tried this for all 3 sentences, and obtained identical results.

### Example Sentences:
1. [MASK] dog sat on the table.
2. The dog savoured [MASK] gram of the food.
3. I own [MASK] dogs.

