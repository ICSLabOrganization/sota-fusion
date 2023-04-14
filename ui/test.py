import tkinter as tk
import pygame
import os

pygame.init()
pygame.display.set_mode((500, 500))

root = tk.Tk()
root.geometry('500x500')

frame = tk.Frame(root, width=500, height=500)
frame.pack()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            root.quit()
    pygame.display.update()
