import neat
import pygame

from game import Game

import os



class BinoGame:
    def __init__(self, window, window_width, window_height):
        self.game = Game(window, window_width, window_height)
        self.level = self.game.level
        self.player = self.game.player
        self.enemy = self.game.enemy
        

    def train_ai(self, genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            output = net.activate([self.player.rect.centery, self.enemy.x])
            decision = output.index(max(output))
            match decision:
                case 0:
                    pass
                case 1:
                    self.game.player.jump()
            self.game.update()
            self.game.draw()
            pygame.display.flip()
            if self.game.playing == False or self.game.score == 100:
                break

        genome.fitness += self.game.score
def eval_genomes(genomes, config):
    width, height = 800, 600
    window = pygame.display.set_mode((width, height))

    for i, (genome_id, genome) in enumerate(genomes):
        genome.fitness = 0
        if i == len(genomes) - 1:
            break
        game = BinoGame(window, width, height)
        game.train_ai(genome, config)

def run_neat(config):
    #p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-43')
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    winner = p.run(eval_genomes, 50)
    # with open("best.pickle", "wb") as f:
    #     pickle.dump(winner, f)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    run_neat(config)
    # test_ai(config)
