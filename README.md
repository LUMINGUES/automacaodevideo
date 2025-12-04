

# 🚀 Gerador Automático de Vídeos com Overlay (Slideshow + GIF)

Este script Python automatiza a criação de vídeos dinâmicos a partir de um conjunto de imagens, otimizando o processo de produção de conteúdo padronizado e rápido.

Ideal para **Reels**, **TikTok**, **Shorts** e vídeos promocionais curtos que exigem um formato consistente.

-----

## ✨ Funcionalidades Principais

  * **Slideshow Automático:** Transforma uma série de imagens estáticas em um vídeo fluido.
  * **Trilha Sonora (Opcional):** Adiciona áudio de fundo ao vídeo final.
  * **Overlay GIF Transparente:** Adiciona um GIF animado em *loop* sobre as imagens, mantendo a transparência (*mask*).
  * **Segmentação Inteligente:** Divide automaticamente o conteúdo em vídeos de **duração máxima definida** (padrão: 30s) para se adequar aos limites de plataformas sociais.

-----

## 🧰 Requisitos e Instalação

Para rodar este projeto, você precisa do **Python 3.x** e da biblioteca `moviepy`.

### Instalação

Abra o terminal ou prompt de comando e instale a dependência:

```bash
pip install moviepy
```

> **Atenção:** A biblioteca `moviepy` utiliza o **FFmpeg** para processamento de vídeo. Em caso de erros de renderização, pode ser necessário instalar o FFmpeg separadamente e garantir que ele esteja no seu `PATH` do sistema.

-----

## ⚙️ Configuração e Uso Rápido

O script foi projetado para ser executado sem argumentos, dependendo de uma estrutura de pastas simples para encontrar todos os arquivos de mídia.

### 1\. Estrutura de Pastas

Crie uma pasta chamada **`imgs/`** no mesmo diretório do script principal.

```
/SeuProjeto/
├── criar_videos_overlay_fix.py  <-- O Script de Geração
└── imgs/                      <-- 📂 PASTA OBRIGATÓRIA PARA AS MÍDIAS
    ├── 01.jpg                 <-- Imagens do Slideshow (Fundo)
    ├── 02.png
    ├── 03.jpg
    ├── trilha_sonora.mp3      <-- Trilha Sonora (Opcional)
    └── logo_animada.gif       <-- Overlay Animado (Opcional)
```

### 2\. Arquivos de Mídia Aceitos

| Tipo de Mídia | Extensões Aceitas | Comentários |
| :--- | :--- | :--- |
| **Imagens (Fundo)** | `.png`, `.jpg`, `.jpeg`, `.bmp`, `.tiff` | Serão ordenadas por **nome do arquivo** (ex: `01.jpg`, `02.jpg`). |
| **Áudio (Trilha Sonora)** | `.mp3`, `.wav` | **Apenas o primeiro** arquivo de áudio encontrado será utilizado. |
| **Overlay (GIF Animado)** | `.gif` | **Apenas o primeiro** GIF encontrado será usado. **É crucial que ele tenha transparência** (`has_mask=True`). |

### 3\. Execução

Execute o script no seu terminal. Os vídeos finais serão salvos dentro da pasta `imgs/`.

```bash
python criar_videos_overlay_fix.py
```

**Saída de Exemplo:**

```
[moviepy] Processamento iniciado...
[moviepy] Lendo 6 imagens no total.
[moviepy] GIF encontrado: logo_animada.gif
[moviepy] Gerando vídeo 1 de 2: video_overlay_1.mp4 (Duração: 30.0s)
[moviepy] Gerando vídeo 2 de 2: video_overlay_2.mp4 (Duração: 15.0s)
[moviepy] Concluído.
```

-----

## 🛠️ Variáveis de Configuração (Ajustes Rápidos)

Ajuste o comportamento do vídeo editando estas variáveis no início do script `criar_videos_overlay_fix.py`:

| Variável | Descrição | Valor Padrão |
| :--- | :--- | :--- |
| `tempo_por_imagem` | Duração de exibição de **cada imagem** no slideshow (em segundos). | `2.5` |
| `tempo_max_video` | **Duração máxima** de cada vídeo de saída. Define o ponto de corte para segmentação. | `30` |
| `fator_redimensionar_gif` | Fator para redimensionar o GIF de overlay. Use `None` para manter o tamanho original ou um decimal (ex: `0.5` para 50%). | `None` |

-----

## 🌟 Detalhes Técnicos e Solução Inovadora

O script resolve de maneira robusta um desafio comum da biblioteca `moviepy` ao trabalhar com *loops* e transparência em GIFs.

### Solução para Loops de GIF Transparentes

1.  **Garantia de Transparência:** O clipe do GIF é lido com `VideoFileClip(..., has_mask=True)` para interpretar o canal *alpha* do GIF.
2.  **Loop Estável:** Em vez de usar o método `.loop()`, que pode causar erros de recursão em ambientes de produção, o script calcula o número de repetições necessárias e usa a função **`concatenate_videoclips`** para criar um único clipe longo e estável para o *overlay*.
      * Este clipe longo é então cortado (`.subclip()`) para ter a **duração exata** do clipe de fundo.

Esta abordagem garante um *overlay* de GIF em *loop* perfeito e transparente sem falhas de renderização.

