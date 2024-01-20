Sirocco
==

# Objectives
- Train technicals skills:
  - Python project setup : pyenv, poetry (opt: ruff, Mypy)
  - JS (frontend) project setup with Vue 3, Nuxt 3, Vuetify 3

- Learn:
  - VueJS composition API
  - Bases for GenAI/LLM : OpenAI, MistralAI, Langchain (opt: HuggingFace transformers)

- Explore:
  - TinyDB: Simple in-memory/on-file database but not a vector store 
  - Pinecone: Seems great (not tested) but no local database 
  - LanceDB: Seems great but smaller community than ChromaDB
  - ChromaDB:  Great fit ! Easy to use

# Todo
## Project setup
- [x] Python development environment with:
    - [x] Poetry for dependency management
    - [x] Pytest for testing
- [x] Going further
    - [x] Ruff for static analysis & code formatting
    - [x] Mypy for type checking

## Features
- [x] Create course
  - [x] Create course
  - [x] Save
  - [x] Update
  - [x] Save On-disk
- [x] Edit course metadata
- [x] Edit course modules (table of contents)
- [x] Content creation
  - [x] Course contents
    - [x] header
    - [x] paragraph
- [ ] Better content
  - [x] RAG generation ==> Too slow !
  - [ ] Regenerate


## Techs
- [ ] Docker + Compose
- [x] Code/Archi cleanup 
- [ ] Vector Store (Pinecode or LanceDB ?) repository
- [x] Choose : Raw (OpenAI, MistralAI), Langchain, Huggingface
  - [x] First draft : Langchain
  - [x] Raw
- [ ] Manage Max tokens with tiktoken ==> Still a draft


## Documentations
- [x] Dev guide
- [x] Python project setup
- [ ] JS project setup

## Later
- [ ] Menu: document (default)
- [ ] Quick chat: (Overlay: simple/single question)
- [ ] Delete course, chapters
- [ ] Real DB
- [ ] Search => vector store ?
- [ ] Import .pdf, notes, ... Connector ?
- [ ] Model Course > Module > Chapter
- [ ] GenAI abstraction !

## Better writing

### Info
Quel est le sujet de votre cours ? S’insère-t-il dans un thème plus global ? Si oui, lequel ?
Que voulez-vous que les inscrits à votre cours en retiennent, sachent faire après avoir suivi votre cours ? Faites une liste, la plus précise possible.
Compétences : les compétences que votre cours doit permettre d’acquérir ;
mots-clés, idées, concepts, morceaux de phrases

### Content guidelines
Privilégiez des phrases courtes
Des phrases courtes, c'est plus digeste. Faites-le ! Vous donnerez des temps de respiration aux apprenants.
Autant que possible, utilisez un vocabulaire simple, que tout le monde peut comprendre.

Attention, il ne faut pas non plus que cela vous empêche d'aborder des notions techniques.
Seulement, prenez le temps de les expliquer et de toujours donner la définition d'un terme qui pourrait poser question.

### Ton
Il faut pouvoir avoir un niveau de langage correct, professionnel tout en restant "proche" des apprenants
vous ne pouvez pas être trop familier en utilisant des mots comme "vachement".

mais vous devez rester accessible, être chaleureux
s'adresser aux apprenants via le vouvoiement (politesse ou collectif) VS le tutoiement,
parler à la 1ère personne du singulier (Je) VS à la 1ère personne du pluriel. (Nous).

# Dev guide
Python project setup
```bash
pyenv local 3.10.4
poetry install
```

Run linter (ruff)
```bash
ruff check .                        
```

Run static type checker
```bash
mypy .                        
```

# Notes on project setup
## Python development environment
Install pyenv & poetry :
```bash
curl https://pyenv.run | bash
curl -sSL https://install.python-poetry.org | python3 -
```

Install python 3.10.4 :
```bash
pyenv install 3.10.4
```

Create new directory and set python version to 3.10.4
```bash
mkdir sirocco
cd sirocco
pyenv local 3.10.4
```

Init poetry project:
```bash
poetry init
poetry shell
```


## JS development environment
TODO !