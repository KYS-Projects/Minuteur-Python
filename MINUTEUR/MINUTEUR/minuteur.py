import os.path
import pygame
import sys

pygame.init()

# Définition des dimensions de la fenêtre
LARGEUR, HAUTEUR = 900, 600
ECRAN = pygame.display.set_mode((LARGEUR, HAUTEUR))

CHEMIN_R = "media"

def getRessource(ressource):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, CHEMIN_R, ressource)

class Bouton():
    def __init__(self, surface=None, pos=None, largeur=None, hauteur=None, texte=None, police=None, couleur_base=None,
                 couleur_survol=None):
        self.surface = surface
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.largeur = largeur
        self.hauteur = hauteur
        self.police = police
        self.couleur_base, self.couleur_survol = couleur_base, couleur_survol
        self.texte = texte
        self.texte_affiche = self.police.render(self.texte, True, self.couleur_base)
        if self.surface is None:
            self.surface = self.texte_affiche
        else:
            self.surface = pygame.transform.smoothscale(self.surface, (largeur, hauteur))
        self.rect = self.surface.get_rect(center=(self.x_pos, self.y_pos))
        self.rect_texte = self.texte_affiche.get_rect(center=(self.x_pos, self.y_pos))

    def mettre_a_jour(self, ecran):
        if self.surface is not None:
            ecran.blit(self.surface, self.rect)
            ecran.blit(self.texte_affiche, self.rect_texte)

    def verifier_entree(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changer_couleur(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.texte_affiche = self.police.render(self.texte, True, self.couleur_survol)
        else:
            self.texte_affiche = self.police.render(self.texte, True, self.couleur_base)

image_de_fond = pygame.image.load(getRessource("a_plan.png")).convert()
icone = pygame.image.load(getRessource("icone.png"))
pygame.display.set_icon(icone)

pygame.display.set_caption("Minuteur")

# Chargement des ressources
FOND = pygame.image.load(getRessource("backdrop.png"))
BOUTON_BLANC = pygame.image.load(getRessource("button.png"))

# Configuration de la police et du texte du minuteur
POLICE_GRANDE = pygame.font.Font(getRessource("ArialRoundedMTBold.ttf"), 120)
POLICE_PETITE = pygame.font.Font(getRessource("ArialRoundedMTBold.ttf"), 20)
texte_minuteur = POLICE_GRANDE.render("00:00:00", True, "white")
texte_minuteur_rect = texte_minuteur.get_rect(center=(LARGEUR / 2, HAUTEUR / 2 - 25))

# Création du bouton de démarrage/pause
Bouton_DP = Bouton(BOUTON_BLANC, (LARGEUR / 2 - 100, HAUTEUR / 2 + 130), 170, 60, "DÉMARRER", POLICE_PETITE, "#c97676",
                   "#1c2747")

# Création du bouton annuler
Bouton_A = Bouton(BOUTON_BLANC, (LARGEUR / 2 + 100, HAUTEUR / 2 + 130), 170, 60, "ANNULER", POLICE_PETITE, "#c97676",
                  "#1c2747")

# Initialisation des variables de temps
heures = 0
minutes = 0
secondes = 0
secondes_actuelles = heures * 3600 + minutes * 60 + secondes

# Ajoutez une nouvelle variable pour suivre l'état de visibilité des boutons
boutons_visibles = True

pygame.time.set_timer(pygame.USEREVENT, 1000)
demarre = False

# Création des boutons pour augmenter et diminuer les heures, les minutes et les secondes
augmenter_heures = Bouton(None, (LARGEUR / 2 - 200, HAUTEUR / 2 - 120), 65, 20, "+", POLICE_GRANDE, "#e6e6e6",
                          "#1c2747")
diminuer_heures = Bouton(None, (LARGEUR / 2 - 200, HAUTEUR / 2 + 50), 65, 20, "-", POLICE_GRANDE, "#e6e6e6", "#1c2747")
augmenter_minutes = Bouton(None, (LARGEUR / 2, HAUTEUR / 2 - 120), 65, 20, "+", POLICE_GRANDE, "#e6e6e6", "#1c2747")
diminuer_minutes = Bouton(None, (LARGEUR / 2, HAUTEUR / 2 + 50), 65, 20, "-", POLICE_GRANDE, "#e6e6e6", "#1c2747")
augmenter_secondes = Bouton(None, (LARGEUR / 2 + 200, HAUTEUR / 2 - 120), 65, 20, "+", POLICE_GRANDE, "#e6e6e6",
                            "#1c2747")
diminuer_secondes = Bouton(None, (LARGEUR / 2 + 200, HAUTEUR / 2 + 50), 65, 20, "-", POLICE_GRANDE, "#e6e6e6",
                           "#1c2747")

# Chargement des sons
son_15min = pygame.mixer.Sound(getRessource("son_15min.wav"))
son_10min = pygame.mixer.Sound(getRessource("son_10min.wav"))
son_5min = pygame.mixer.Sound(getRessource("son_5min.wav"))
son_2min = pygame.mixer.Sound(getRessource("son_2min.wav"))
son_1min = pygame.mixer.Sound(getRessource("son_1min.wav"))
son_fin = pygame.mixer.Sound(getRessource("son_fin.wav"))

# Boucle principale
while True:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evenement.type == pygame.MOUSEBUTTONDOWN:
            if Bouton_DP.verifier_entree(pygame.mouse.get_pos()):
                demarre = not demarre
                boutons_visibles = False  # Les boutons ne sont pas visibles lorsque le minuteur démarre ou est en pause
                Bouton_DP.texte = "PAUSE" if demarre else "DÉMARRER"
                Bouton_DP.texte_affiche = POLICE_PETITE.render(Bouton_DP.texte, True, Bouton_DP.couleur_base)
                Bouton_DP.mettre_a_jour(ECRAN)
            elif Bouton_A.verifier_entree(pygame.mouse.get_pos()):
                heures = minutes = secondes = 0
                secondes_actuelles = heures * 3600 + minutes * 60 + secondes
                demarre = False
                boutons_visibles = True  # Rendre les boutons visibles lorsque "Annuler" est cliqué
                Bouton_DP.texte = "DÉMARRER"
                Bouton_DP.texte_affiche = POLICE_PETITE.render(Bouton_DP.texte, True, Bouton_DP.couleur_base)
                Bouton_DP.mettre_a_jour(ECRAN)

            # Ajout de la logique pour les boutons d'augmentation et de diminution des heures
            if boutons_visibles:
                if augmenter_heures.verifier_entree(pygame.mouse.get_pos()):
                    heures = (heures + 1) % 24
                elif diminuer_heures.verifier_entree(pygame.mouse.get_pos()):
                    heures = (heures - 1) % 24 if heures > 0 else 23
                if augmenter_minutes.verifier_entree(pygame.mouse.get_pos()):
                    minutes = (minutes + 1) % 60
                elif diminuer_minutes.verifier_entree(pygame.mouse.get_pos()):
                    minutes = (minutes - 1) % 60 if minutes > 0 else 59
                if augmenter_secondes.verifier_entree(pygame.mouse.get_pos()):
                    secondes = (secondes + 1) % 60
                elif diminuer_secondes.verifier_entree(pygame.mouse.get_pos()):
                    secondes = (secondes - 1) % 60 if secondes > 0 else 59
                secondes_actuelles = heures * 3600 + minutes * 60 + secondes
        if evenement.type == pygame.USEREVENT and demarre:
            if secondes_actuelles > 0:
                # Jouer les sons à des intervalles spécifiques
                if secondes_actuelles == 15 * 60:
                    son_15min.play()
                elif secondes_actuelles == 10 * 60:
                    son_10min.play()
                elif secondes_actuelles == 5 * 60:
                    son_5min.play()
                elif secondes_actuelles == 2 * 60:
                    son_2min.play()
                elif secondes_actuelles == 1 * 60:
                    son_1min.play()

                secondes_actuelles -= 1
            else:
                # Jouer le son de fin lorsque le minuteur atteint 0
                son_fin.play()
                demarre = False
                boutons_visibles = True  # Rendre les boutons visibles lorsque le minuteur atteint 00:00:00
                Bouton_DP.texte = "DÉMARRER"
                Bouton_DP.texte_affiche = POLICE_PETITE.render(Bouton_DP.texte, True, Bouton_DP.couleur_base)
                Bouton_DP.mettre_a_jour(ECRAN)

    # Mise à jour de l'affichage du minuteur
    heures_affichees = int(secondes_actuelles / 3600)
    minutes_affichees = int((secondes_actuelles % 3600) / 60)
    secondes_affichees = secondes_actuelles % 60
    texte_minuteur = POLICE_GRANDE.render(f"{heures_affichees:02}:{minutes_affichees:02}:{secondes_affichees:02}", True,
                                          "white")
    texte_minuteur_rect = texte_minuteur.get_rect(center=(LARGEUR / 2, HAUTEUR / 2 - 25))

    ECRAN.blit(image_de_fond, (0, 0))
    ECRAN.blit(FOND, FOND.get_rect(center=(LARGEUR / 2, HAUTEUR / 2)))

    Bouton_DP.mettre_a_jour(ECRAN)
    Bouton_A.mettre_a_jour(ECRAN)
    Bouton_DP.changer_couleur(pygame.mouse.get_pos())
    Bouton_A.changer_couleur(pygame.mouse.get_pos())

    augmenter_heures.changer_couleur(pygame.mouse.get_pos())
    diminuer_heures.changer_couleur(pygame.mouse.get_pos())
    augmenter_minutes.changer_couleur(pygame.mouse.get_pos())
    diminuer_minutes.changer_couleur(pygame.mouse.get_pos())
    augmenter_secondes.changer_couleur(pygame.mouse.get_pos())
    diminuer_secondes.changer_couleur(pygame.mouse.get_pos())

    # Afficher les boutons d'heures, minutes et secondes seulement si le minuteur est arrêté ou a atteint 00:00:00
    if boutons_visibles or (not demarre and secondes_actuelles == 0):
        augmenter_heures.mettre_a_jour(ECRAN)
        diminuer_heures.mettre_a_jour(ECRAN)
        augmenter_minutes.mettre_a_jour(ECRAN)
        diminuer_minutes.mettre_a_jour(ECRAN)
        augmenter_secondes.mettre_a_jour(ECRAN)
        diminuer_secondes.mettre_a_jour(ECRAN)

    ECRAN.blit(texte_minuteur, texte_minuteur_rect)
    pygame.display.update()
    pygame.time.Clock().tick(30)

