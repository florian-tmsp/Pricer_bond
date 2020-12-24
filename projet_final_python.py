# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 16:46:37 2020

@author: Florian_Goupil
"""
#import pandas as pd
import math
import matplotlib.pyplot as plt


#taux_equivalent = taux/frequence

class Bond:
#La valeur nominale est la valeur comptable qui a été initialement prêtée. Elle sert de référence pour le calcul du remboursement et des intérêts.
#La maturité ou maturité résiduelle désigne le temps qui sépare la date à laquelle une obligation est émise, et la date à laquelle la valeur nominale de cette obligation est remboursée.
#Yield To Maturity correspond au calcul du taux de rendement que rapporte à l'échéance un investissement effectué dans un produit de taux (principalement les obligations)
    def __init__(self, nominal, maturite, coupon, taux, frequence):
        self.nominal = nominal
        self.maturite = maturite
        self.coupon = coupon
        self.taux = taux
        self.frequence = frequence
    
    def get_taux(self):
        taux_equivalent = self.taux/self.frequence    #((1+taux)**(1/frequence))-1 #taux/frequence
        return taux_equivalent
    
    def get_prix(self):
        flux = []        
        for i in range(1, self.frequence*self.maturite):
            #flux.append((coupon/frequence*nominal)*math.exp(-self.get_taux()*i))            
            flux.append((self.coupon/self.frequence*self.nominal)/(1+self.get_taux())**i)
        flux.append((self.nominal+(self.coupon/self.frequence*self.nominal))/((1+self.get_taux())**(self.maturite*self.frequence)))
        #flux.append(((nominal)+((coupon/frequence)*nominal))*math.exp(-self.get_taux()*maturite*frequence))
        return flux
    
    
    def get_flux_annuel(self):
        flux = []
        
        for i in range(1, self.maturite):
            #flux.append((coupon/frequence*nominal)*math.exp(-self.get_taux()*i))            
            flux.append((self.coupon*self.nominal)/((1+self.taux)**i))
        flux.append((self.nominal+(self.coupon*self.nominal))/((1+self.taux)**(self.maturite)))
        #flux.append(((nominal)+((coupon/frequence)*nominal))*math.exp(-self.get_taux()*maturite*frequence))
        return flux

#http://financedemarche.fr/finance/comment-calculer-la-duration-dune-obligation-definition-formule    
    def get_duration(self):
        flux_actualise = []
        poids = []
        date_poids = []
        flux_actualise = self.get_prix()
        for k in range(0, len(flux_actualise)):
            poids.append(flux_actualise[k]/sum(flux_actualise))        
        for j in range(0, len(self.get_flux_annuel())):
            date_poids.append((j+1)*poids[j])
        return sum(date_poids)

    def get_sensibilite(self):
        sensibilite = -self.get_duration()/(1+self.taux)
        return sensibilite

#https://www.iotafinance.com/Formule-convexite-d-une-obligation.html
    def get_convexite(self):
        value_prix = []
        value_taux = [self.taux]
        value_taux.append(value_taux[0]-0.0001)        
        value_taux.append(value_taux[0]+0.0001)
        value_taux = sorted(value_taux)
        for s in range(0, len(value_taux)):
            value_prix.append(((((self.coupon*self.nominal)/self.frequence)*((1-(1+value_taux[s]/self.frequence)**(-self.maturite*self.frequence))/(value_taux[s]/self.frequence)))+((self.nominal*(1+value_taux[s]/self.frequence)**(-self.maturite*self.frequence)))))
        convexite = (value_prix[2]+value_prix[0]-(2*value_prix[1]))/(2*value_prix[1]*(0.0001**2))
        return convexite




    def get_duration_effective(self):
        value_tangente = []
        value_prix = []
        value_taux = [self.taux]
        value_taux.append(value_taux[0]-0.0001)        
        value_taux.append(value_taux[0]+0.0001)
        value_taux = sorted(value_taux)
        for s in range(0, len(value_taux)):
            value_prix.append(((((self.coupon*self.nominal)/self.frequence)*((1-(1+value_taux[s]/self.frequence)**(-self.maturite*self.frequence))/(value_taux[s]/self.frequence)))+((self.nominal*(1+value_taux[s]/self.frequence)**(-self.maturite*self.frequence)))))

        duration_effective = (value_prix[0]-value_prix[2])/(2*value_prix[1]*0.0001) #https://analystprep.com/cfa-level-1-exam/fixed-income/macaulay-modified-effective-durations/
        coef_directeur = ((value_prix[2]/value_prix[1])-1)/0.0001


        return duration_effective/100, coef_directeur

    def get_derive(self, value_prix, value_taux, taux):
        pos_taux = value_taux.index(taux)
        dif_y = value_prix[pos_taux]-value_prix[pos_taux+10]
        dif_x = value_taux[pos_taux]-value_taux[pos_taux+10]
        coef = dif_y/dif_x


        """
        print('value pos', pos_taux)
        print('value_prix : ', value_prix)
        print('value_taux : ', value_taux)
        print('value y  : ', dif_y)
        print('value dif_x : ', dif_x)
        print('coef : ', coef)
        """
        return coef
        

    def get_graph(self):
        tangeante = []
        value_prix = []
        value_taux = [0.001]
        value_tangente = []
        
        for i in range(0, 999):
            value_taux.append(value_taux[i]+0.001)
        value_taux.append(self.taux)  
        value_taux = sorted(value_taux)          
        position = value_taux.index(self.taux)
        for s in range(0, len(value_taux)):
            value_prix.append(((((self.coupon*self.nominal)/self.frequence)*((1-(1+value_taux[s]/self.frequence)**(-self.maturite*self.frequence))/(value_taux[s]/self.frequence)))+((self.nominal*(1+value_taux[s]/self.frequence)**(-self.maturite*self.frequence)))))
     

        coef_directeur = (value_prix[position+1]-value_prix[position-1])/0.001
        for l in range(0, len(value_taux)):
            value_tangente.append(coef_directeur*(value_taux[l]-value_taux[position])+value_prix[position])

        return value_prix, value_taux, value_tangente
    
    

#test = Bond(nominal, maturite, coupon, taux, frequence)
#test.get_prix()
#test.get_duration()
#test.get_sensibilite()

#print(sum(test.get_prix()))
#print(test.get_duration())
#print(test.get_sensibilite())

class ZBond:
#La valeur nominale est la valeur comptable qui a été initialement prêtée. Elle sert de référence pour le calcul du remboursement et des intérêts.
#La maturité ou maturité résiduelle (en finance) désigne le temps qui sépare la date à laquelle une obligation est émise, et la date à laquelle la valeur nominale de cette obligation est remboursée.
#Yield To Maturity correspond au calcul du taux de rendement que rapporte à l'échéance un investissement effectué dans un produit de taux (principalement les obligations)
    def __init__(self, nominal, maturite, ytm):
        self.nominal = nominal
        self.maturite = maturite
        self.ytm = ytm
        
    def get_prix(self):
        prix = self.nominal/((1+self.ytm)**self.maturite)
        return prix
    
    def get_duration(self):
        duration = self.maturite
        return duration

    def get_graph(self):
        value_tangente = []
        value_prix = []
        value_taux = [0]
        for i in range(0, 1000):
            value_taux.append(value_taux[i]+0.001)
        value_taux.append(self.ytm)
        value_taux = sorted(value_taux)
        position = value_taux.index(self.ytm)
        for s in range(0, len(value_taux)):
            value_prix.append(self.nominal/((1+value_taux[s])**self.maturite))

        coef_directeur = (value_prix[position+1]-value_prix[position-1])/0.001
        for l in range(0, len(value_taux)):
            value_tangente.append(coef_directeur*(value_taux[l]-value_taux[position])+value_prix[position])



        return value_prix, value_taux, value_tangente

class PBond:
    def __init__(self, nominal, maturite, ytm, coupon):
        self.nominal = nominal
        self.maturite = maturite
        self.ytm = ytm
        self.coupon = coupon
        
    def get_prix(self):
        prix = (self.nominal*self.coupon)/self.ytm
        return prix

    def get_graph(self):
        value_prix = []
        value_taux = [0]
        for i in range(0, 1000):
            value_taux.append(value_taux[i]+0.001)
        value_taux.append(self.ytm)
        value_taux = sorted(value_taux)

        
        for s in range(0, len(value_taux)):
            value_prix.append(self.nominal/((1+value_taux[s])**self.maturite))

        return value_prix, value_taux
    
    
    
    
class Rate:
    
    def __init__(self, valeur, nominal, maturite, coupon, frequence):
        self.nominal = nominal
        self.maturite = maturite
        self.coupon = coupon
        self.valeur = valeur        
        self.frequence = frequence
    """
    def get_TauxActuariel(self):
        rendement = ((self.coupon*self.nominal)/self.valeur)*100
        if self.valeur > self.nominal:
            ytm = rendement-((self.valeur-self.nominal)/self.maturite)
        else:
            ytm = rendement+((self.valeur-self.nominal)/self.maturite)
        ytm = ytm/100
        return ytm
    """

    def get_TauxActuariel(self):
        valeur_actualise = self.valeur
        vecteur_taux = [0.0001]
        vecteur_prix = []
        for j in range(0, 10000):
            vecteur_taux.append(vecteur_taux[j]+0.0001)
        

        for i in range(0, len(vecteur_taux)):
            difference = valeur_actualise - ((((self.coupon*self.nominal)/self.frequence)*((1-(1+vecteur_taux[i]/self.frequence)**(-self.maturite*self.frequence))/(vecteur_taux[i]/self.frequence)))+((self.nominal*(1+vecteur_taux[i]/self.frequence)**(-self.maturite*self.frequence))))

            if abs(difference) < 0.1:
                return round(vecteur_taux[i], 4)


 

    
    def get_taux(self):
        taux_equivalent =((1+self.get_TauxActuariel())**(1/self.frequence))-1 #self.get_TauxActuarielle()/frequence     #taux/frequence
        return taux_equivalent
    
    def get_prix(self):
        flux = []        
        for i in range(1, self.frequence*self.maturite):
            #flux.append((coupon/frequence*nominal)*math.exp(-self.get_taux()*i))            
            flux.append((self.coupon/self.frequence*self.nominal)/(1+self.get_TauxActuariel())**i)
        flux.append((self.nominal+(self.coupon/self.frequence*self.nominal))/((1+self.get_TauxActuariel())**(self.maturite*self.frequence)))
        #flux.append(((nominal)+((coupon/frequence)*nominal))*math.exp(-self.get_taux()*maturite*frequence))
        return sum(flux) 
    """ Question : approximation """
    
    

question = str("Quelle action souhaitez vous effectuer ?\n z --> Valoriez un Zero Coupon\n f --> Valoriez une obligation a taux fixe\n p --> Valoriez une obligation perpetuelle\n r --> Calculer un taux actuariel\n s --> Sortir")
question_z = str('Renseigner : nominal, maturite, ytm (ex 0.02 pour 2%): ')
question_f = str('Renseigner : nominal, maturite, coupon (ex 0.02 pour 2%), taux (ex 0.02 pour 2%), frequence (occurence par année)')
question_p = str('Renseigner : nominal, maturite, ytm (ex 0.02 pour 2%), coupon (ex 0.02 pour 2%)')
question_r = str('Renseigner : valeur, nominal, maturite (en année), coupon (ex 0.02 pour 2%), frequence (occurence par année)')

print(question)

value = input('entrez valeur : ')

reponse_accepte = ['z', 'f', 'p', 'r', 's']

value_pos = reponse_accepte.index(value)

if value_pos == 0:
    print(question_z)
    nominal = int(input('Nominal = '))
    maturite = int(input('maturite = '))
    ytm = float(input('ytm = '))
    zbond = ZBond(nominal, maturite, ytm)
    print('Prix : ' + str(zbond.get_prix()))
    print('Duration : ' + str(zbond.get_duration()))
    liste_prix, liste_taux, liste_tangente = zbond.get_graph()

    plt.plot(liste_taux,liste_prix, color = "red", label="Courbe de prix")
    plt.plot(liste_taux[:-3*len(liste_taux)//4], liste_tangente[:-3*len(liste_taux)//4], color="green", label= "Tangente")
    plt.title("Courbe de prix")
    plt.xlabel("Rate")
    plt.ylabel("Prix")
    plt.legend()
    plt.show()


elif value_pos == 1:
    print(question_f)
    nominal = int(input('Nominal = '))
    maturite = int(input('maturite = '))
    coupon = float(input('coupon = '))
    taux = float(input('taux = '))
    taux = float(taux)
    frequence = int(input('frequence = '))
    fbond = Bond(nominal, maturite, coupon, taux, frequence)
    duration_effective, coef_directeur = fbond.get_duration_effective()
    print('Prix : ' + str(sum(fbond.get_prix())))
    print('Duration : ' + str(fbond.get_duration()))
    print('Sensibilite : ' + str(fbond.get_sensibilite()))
    print('Duration effectiv (Pour 1 pt de base): ' + str(duration_effective))
    print('Convexite : ' + str(fbond.get_convexite()))
    liste_prix, liste_taux, liste_tangente = fbond.get_graph()


    plt.plot(liste_taux,liste_prix, color = "red", label="Courbe de prix")
    plt.plot(liste_taux[:-3*len(liste_taux)//4], liste_tangente[:-3*len(liste_taux)//4], color="green", label= "Tangente")
    plt.title("Courbe de prix")
    plt.xlabel("Rate")
    plt.ylabel("Prix")
    plt.legend()
    plt.show()

elif value_pos == 2:
    print(question_p)
    nominal = int(input('Nominal = '))
    maturite = int(input('maturite = '))
    coupon = float(input('coupon = '))
    ytm = float(input('ytm = '))
    pbond = PBond(nominal, maturite, coupon, ytm)
    print('Prix : ' + str(pbond.get_prix()))
    liste_prix, liste_taux = pbond.get_graph()
    plt.plot(liste_taux, liste_prix)
    plt.xlabel('Rate')
    plt.ylabel('Prix')
    plt.show()   
elif value_pos == 3:
    print(question_f)
    nominal = int(input('Nominal = '))
    maturite = int(input('maturite = '))
    coupon = float(input('coupon = '))
    valeur = float(input('valeur = '))
    frequence = int(input('frequence = '))
    rate = Rate(valeur, nominal, maturite, coupon,  frequence)
    print('Taux actuariel : ' + str(rate.get_TauxActuariel()))
    print('Prix : ' + str(rate.valeur))    
    print('Revalorisation : ' + str(rate.get_prix()))
else:
    pass
    
    


    
    
    
    
