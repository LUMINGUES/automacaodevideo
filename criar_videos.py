import os
import sys
import math

try:
    from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip, VideoFileClip, CompositeVideoClip
except ImportError:
    print("\nERRO CRÍTICO: Biblioteca 'moviepy' não encontrada!")
    sys.exit()

def criar_videos_overlay_fix():
    # --- CONFIGURAÇÕES ---
    pasta_raiz = os.getcwd()
    pasta_alvo = os.path.join(pasta_raiz, 'imgs') 
    
    tempo_por_imagem = 2.5
    tempo_max_video = 30 # <--- ALTERADO PARA 30 SEGUNDOS
    imgs_por_video = int(tempo_max_video / tempo_por_imagem)

    # Configuração de redimensionamento do GIF (None = tamanho original)
    # Se o GIF cobrir a tela toda e você quiser diminuir, mude para ex: 0.3
    fator_redimensionar_gif = None 

    extensoes_img = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')
    extensoes_audio = ('.mp3', '.wav')
    extensoes_gif = ('.gif',)

    if not os.path.exists(pasta_alvo):
        print(f"ERRO: Pasta '{pasta_alvo}' não encontrada!")
        return

    # 1. Carrega Arquivos
    arquivos_img = [f for f in os.listdir(pasta_alvo) if f.lower().endswith(extensoes_img)]
    arquivos_img.sort()
    
    if not arquivos_img:
        print("Nenhuma imagem encontrada.")
        return

    # Procura Áudio
    arquivos_audio = [f for f in os.listdir(pasta_alvo) if f.lower().endswith(extensoes_audio)]
    caminho_audio = os.path.join(pasta_alvo, arquivos_audio[0]) if arquivos_audio else None
    
    # Procura GIF
    arquivos_gif = [f for f in os.listdir(pasta_alvo) if f.lower().endswith(extensoes_gif)]
    caminho_gif = os.path.join(pasta_alvo, arquivos_gif[0]) if arquivos_gif else None

    if caminho_gif:
        print(f"GIF DE OVERLAY: '{arquivos_gif[0]}'")

    total_imagens = len(arquivos_img)
    contador_video = 1

    # 2. Processamento
    for i in range(0, total_imagens, imgs_por_video):
        lote_arquivos = arquivos_img[i : i + imgs_por_video]
        clips_imagens = []
        
        print(f"\n--- Processando Vídeo {contador_video} ---")

        # A) Monta o fundo (Slideshow)
        for nome_arquivo in lote_arquivos:
            caminho_completo = os.path.join(pasta_alvo, nome_arquivo)
            clip = ImageClip(caminho_completo).set_duration(tempo_por_imagem)
            # clip = clip.resize(height=1080) # Se precisar forçar altura
            clips_imagens.append(clip)
            print(f"Frame: {nome_arquivo}")

        if clips_imagens:
            video_fundo = concatenate_videoclips(clips_imagens, method="compose")
            duracao_video = video_fundo.duration
            
            # Lista de camadas: [Fundo, GIF]
            elementos_video = [video_fundo]

            # B) Monta o GIF (Correção do erro de recursão)
            gif_final = None
            if caminho_gif:
                try:
                    # has_mask=True é OBRIGATÓRIO para o Python não deixar o fundo preto
                    gif_base = VideoFileClip(caminho_gif, has_mask=True)
                    
                    # 1. Calcula quantas vezes o GIF cabe no vídeo
                    qtd_repeticoes = math.ceil(duracao_video / gif_base.duration)
                    
                    # 2. Cria uma lista clonando o GIF várias vezes
                    lista_gifs = [gif_base] * qtd_repeticoes
                    
                    # 3. Junta tudo num clipe longo (Isso evita o bug do .loop())
                    gif_longo = concatenate_videoclips(lista_gifs, method="compose")
                    
                    # 4. Corta o excesso
                    gif_final = gif_longo.subclip(0, duracao_video)
                    
                    # Redimensiona se configurado
                    if fator_redimensionar_gif:
                        gif_final = gif_final.resize(fator_redimensionar_gif)
                    
                    # Adiciona na lista de camadas
                    elementos_video.append(gif_final)
                    print("GIF aplicado com transparência.")
                    
                except Exception as e:
                    print(f"Erro no GIF: {e}")

            # C) Junta Fundo + GIF
            video_completo = CompositeVideoClip(elementos_video)

            # D) Coloca Áudio
            audio_clip = None
            if caminho_audio:
                try:
                    audio_clip = AudioFileClip(caminho_audio)
                    # Ajusta duração do áudio
                    if audio_clip.duration > duracao_video:
                        audio_clip = audio_clip.subclip(0, duracao_video)
                    video_completo = video_completo.set_audio(audio_clip)
                except Exception as e:
                    print(f"Erro no áudio: {e}")

            # E) Salva
            nome_saida = f"video_overlay_{contador_video}.mp4"
            caminho_saida = os.path.join(pasta_alvo, nome_saida)
            
            # Preset ultrafast para renderizar rápido
            video_completo.write_videofile(
                caminho_saida, 
                fps=24, 
                codec='libx264', 
                audio_codec='aac',
                preset='ultrafast'
            )

            # Limpeza
            if audio_clip: audio_clip.close()
            if gif_final: gif_final.close()
            # gif_base.close() # Pode causar erro se fechar antes do concatenate terminar internamente
            
            contador_video += 1

    print("\nConcluído!")

if __name__ == "__main__":
    criar_videos_overlay_fix()