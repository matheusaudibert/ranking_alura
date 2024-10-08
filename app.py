import streamlit as st
import datetime

def parse_txt(filename):
    projects = []
    
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
    
    blocks = content.split('Novo projeto recebido!\n')
    
    for block in blocks[1:]: 
        
        name_start = block.find('Nome\n') + len('Nome\n')
        name_end = block.find('\n', name_start)
        name = block[name_start:name_end].strip()
        
        link_start = block.find('Link do github com o projeto\n') + len('Link do github com o projeto\n')
        link_end = block.find('\n', link_start)
        github_link = block[link_start:link_end].strip()
        
        description_start = block.find('Descrição do projeto\n') + len('Descrição do projeto\n')
        description_end = block.find('\n', description_start)
        description = block[description_start:description_end].strip()
        
        reactions = 0
      
        reactions_start = block.find('{Reactions}\n⭐ (') + len('{Reactions}\n⭐ (')
        if reactions_start > len('{Reactions}\n⭐ ('):
            reactions_end = block.find(')', reactions_start)
            try:
                reactions = int(block[reactions_start:reactions_end].strip())
            except ValueError:
                reactions = 0
        
        projects.append((name, github_link, reactions))
    
    sorted_projects = sorted(projects, key=lambda x: x[2], reverse=True)
    
    return sorted_projects

def display_projects(st, title, projects, start_index):
    st.markdown(title)
    for i, (name, github_link, reactions) in enumerate(projects, start=start_index):
        st.markdown(f"{i}. **Nome**: {name}")
        st.markdown(f"   **Link do Projeto**: [Link]({github_link})")
        st.markdown(f"   **Reações**: :orange[{reactions}]")


def main():
    st.set_page_config(page_title="Ranking Imersão Dev", layout="wide", initial_sidebar_state="expanded", menu_items=None)

    st.title("🏆 Ranking Imersão Dev :gray[(Não Oficial)]")

    input_filename = 'ranking.txt'
    projects = parse_txt(input_filename)
    top_30_projects = projects[:30]

    col1, col2, col3 = st.columns(3)
   
    top_10 = top_30_projects[:10]
    top_20 = top_30_projects[10:20]
    top_30 = top_30_projects[20:30]

    with col1:
        display_projects(st, "#", top_10, start_index=1)
    
    with col2:
        display_projects(st, "#", top_20, start_index=11)
    
    with col3:
        display_projects(st, "#", top_30, start_index=21)

    st.markdown("### 📚 Total de projetos: 1677")

    with st.sidebar:
      st.markdown(f"### ⏳ :red[Votações Encerradas]")

    st.sidebar.header("🔍 Pesquisar Projeto")
    search_name = st.sidebar.text_input("Digite o seu nome:")
    
    if search_name:
        results = []
        for index, (name, github_link, reactions) in enumerate(projects):
            if search_name.lower() in name.lower():
                results.append((index + 1, name, github_link, reactions))
        
        if results:
            with st.sidebar:
                st.sidebar.markdown(f"Resultados para '{search_name}':")
                for position, name, project_link, reactions in results:
                    st.sidebar.markdown(f"{position}. **Nome**: {name}")
                    st.sidebar.markdown(f"   **Link do Projeto**: [Link]({project_link})")
                    st.sidebar.markdown(f"   **Reações**: :orange[{reactions}]")
        else:
            with st.sidebar:
                st.sidebar.markdown("Não te encontrei.")

    with st.sidebar:
      st.markdown(f"🌐 [Acesse o meu projeto](https://devspaceee.vercel.app/index.html)")
      st.markdown(f"🤿 [Imersão Dev [Guia de Mergulho]](https://grupoalura.notion.site/Imers-o-Dev-com-Gemini-Guia-de-Mergulho-7742af09c51649348a91f67157df8a41#fbfa928f2b37444b91c995f7e00e8f58)")
      st.markdown(f"📋 [Regulamento](https://docs.google.com/document/d/19aLXZBDHmBx3RtYIL0ukTa9MFmnyx_G-/edit)")

if __name__ == "__main__":
    main()