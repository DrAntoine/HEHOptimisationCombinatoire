
fonction validation(individu):
    si coherent(individu):
        retourne estimation_prix(individu)
    sinon:
        retourne -1

fonction coherence(individu):
    check :
        nombre plaque > 0
        pour chaque plaque:
            nombre impression plaque > 0
            nombre de slot utilisé <= nombre slot max
            couverture dans slot présente dans liste de couverture
        verification contrainte nb impression respectée
    retourne vrai/faux

fonction estimation_prix(individu):
    retourne nb_plaque * prix plaque + nb feuilles * prix feuille

fonction mixage(individu1, individu2, mutation_nb_chromo, mutation_chromo):
    new_nb_chromo = nb_chromo1+nb_chromo2/2
    si (random number[0:1])<mutation_chromo:
        new_nb_chromo += choice[-1;1]
    all_chromo = chromo1+chromo2
    new_chromo = []
    for i in range(new_nb_chromo):
        chromo_selected = choice(all_chromo)
        muted_chromo = mutate(chromo_selected, mutation_chromo)
        new_nb_chromo.append(muted_chromo)
    retourne new_chromo

fonction mutate(chromosome, mutation_chromo):
    nb_copie = chromosome[0]
    agencement = chromosome[1:]
    si (random number[0:1]<mutation_chromo):

    