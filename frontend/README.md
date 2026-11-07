# 🎓 Ensalamento Digital - Front-end Web

Bem-vindos ao repositório do Front-end do projeto **Ensalamento Digital**! 

Este módulo da nossa aplicação concentra duas interfaces essenciais:
1. **Painel da TV (Digital Signage)**: Tela em modo *Kiosk* (tela cheia) para a sala dos professores.
2. **Web Administrativo**: Sistema protegido por login para a coordenação gerenciar as alocações.

---

## 🛠️ Nossa Stack (Tecnologias Usadas)

Como estamos no 2º período, escolhemos tecnologias modernas e eficientes, mas fáceis de entender se você pegar o conceito básico. Se você estiver "voando" em alguma delas, leia este resumo:

* **React + Vite + TypeScript**: Nossa base. O Vite deixa o projeto super rápido de rodar, e o TypeScript (uso de tipagens) evita que a gente mande dados errados para a API, ajudando a pegar erros antes mesmo de salvar o arquivo.
* **Tailwind CSS**: Em vez de criar arquivos `.css` separados, estilizamos os componentes escrevendo classes diretamente no HTML/JSX (ex: `className="bg-blue-500 text-white"`).
* **shadcn/ui (⚠️ Muito Importante!)**: O shadcn não é uma biblioteca comum que você importa do `node_modules`. Ele injeta o código-fonte do componente direto na nossa pasta `src/components/ui/`. Se você precisar de um botão ou formulário, não crie do zero: importe o `<Button />` ou `<Input />` que já estão configurados na nossa pasta. **Regra:** Tente não modificar a lógica interna desses arquivos base, apenas os utilize nas páginas.
* **Zustand**: Sabe quando precisamos guardar uma informação global que várias telas vão usar, tipo o "usuário logado" ou o "token"? Em vez de usar Context API complexa ou Redux, usamos o Zustand. É muito simples, e fica tudo salvo na nossa pasta `stores/`.
* **Axios**: É a biblioteca que usamos para fazer as requisições (GET, POST) para a nossa API no Back-end (Django).
* **ESLint + Prettier**: Ferramentas que "vigiam" nosso código para garantir que todos estão escrevendo no mesmo padrão, arrumando espaçamentos e erros sozinhos (se o seu VS Code estiver configurado certo).

---

## 📂 Estrutura de Pastas

Para manter a organização do nosso repositório, a arquitetura principal dentro de `src/` funciona assim:

| Pasta / Arquivo | O que é e para que serve? |
| :--- | :--- |
| 🧩 `components/ui/` | Contém exclusivamente os componentes visuais de interface gerados automaticamente pelo shadcn/ui. São os blocos de montar da aplicação. |
| 🖼️ `layouts/` | Estruturas de "casca" para as páginas. Aqui ficam os componentes que encapsulam rotas para adicionar barras de navegação laterais, cabeçalhos ou injetar provedores de contexto globais. |
| 📄 `pages/` | As telas finais do sistema. As pastas aqui dentro refletem os domínios da nossa aplicação (telas públicas, telas protegidas da coordenação, painel da TV, etc.). |
| 📦 `stores/` | Responsável pelo gerenciamento de estado global da aplicação usando o Zustand. Guarda informações que precisam sobreviver à navegação entre as telas. |
| ⚙️ `lib/` | Funções utilitárias genéricas, validações e configurações auxiliares que podem ser importadas em qualquer lugar do projeto. |
| 🚦 `router.tsx` | O arquivo centralizador de rotas do React Router Dom. Ele dita qual componente de layout ou página deve ser renderizado quando o usuário acessa uma URL específica. |

---

## ⚙️ Configuração Obrigatória: VS Code

**Pare tudo e faça isso antes de começar a codar!**
Para o código de todo mundo ficar idêntico nos *Pull Requests* (sem conflitos chatos de espaçamento ou importação faltando), configure o seu VS Code para formatar tudo sozinho usando o ESLint quando você salvar:

1. Crie uma pasta chamada `.vscode` na raiz do projeto (perto do `package.json`).
2. Crie um arquivo `settings.json` dentro dela e cole exatamente o código abaixo:

```json
{
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit",
    "source.organizeImports": "explicit"
  },
  "eslint.validate": [
    "javascript",
    "javascriptreact",
    "typescript",
    "typescriptreact"
  ]
}
```
*Mágica: Toda vez que você der `Ctrl + S`, o VS Code, junto com o ESLint, vai formatar as indentações, aspas e organizar as importações no topo do arquivo sozinho.*

---

## 🚀 Como rodar o projeto localmente

Não temos arquivo `.env` (variáveis de ambiente) no momento, então rodar o projeto está bem direto:

1. **Clone o repositório e entre na pasta do front-end:**
   ```bash
   git clone [COLE-O-LINK-DO-GITHUB-AQUI]
   cd frontend
   ```
2. **Instale os pacotes e dependências (usamos NPM):**
   ```bash
   npm install
   ```
3. **Inicie o servidor de desenvolvimento:**
   ```bash
   npm run dev
   ```
4. Abra `http://localhost:5173` no seu navegador.