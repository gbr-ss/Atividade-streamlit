import streamlit as st

# Configuração da página
st.set_page_config(page_title="Ajude os Pets", page_icon="🐾", layout="wide")

# Inicializa sessão
if "pets_para_adocao" not in st.session_state:
    st.session_state.pets_para_adocao = []

if "total_adotados" not in st.session_state:
    st.session_state.total_adotados = 0

if "mostrar_baloes" not in st.session_state:
    st.session_state.mostrar_baloes = False

if "pet_adotado" not in st.session_state:
    st.session_state.pet_adotado = None

# -------------------- META DE ADOÇÃO --------------------
meta_adocao = 20  # meta mensal
adocoes = st.session_state.total_adotados
porcentagem = min(adocoes / meta_adocao, 1.0)

st.subheader("🎯 Meta de adoção do mês")
st.progress(porcentagem)
st.write(f"{adocoes} de {meta_adocao} pets adotados")
st.divider()

# Mostrar mensagem de sucesso e balões se um pet foi adotado
if st.session_state.mostrar_baloes:
    st.success(f"🎉 Você adotou {st.session_state.pet_adotado}!")
    st.balloons()
    st.session_state.mostrar_baloes = False
    st.session_state.pet_adotado = None

# -------------------- ABAS --------------------
aba_consciencia, aba_cadastro, aba_ver = st.tabs([
    "🐾 Conscientização", 
    "📋 Cadastrar Pet", 
    "🐶 Ver Pets para Adoção"
])

# -------------------- ABA DE CONSCIENTIZAÇÃO --------------------
with aba_consciencia:
    st.title("🐾 Ajude os Pets")
    st.write("Escolha um animal para saber como ajudar:")
    
    options = ["Gato", "Cachorro", "Furão"]
    selection = st.radio("Selecione um animal:", options)

    if selection:
        if selection == "Gato":
            st.header("🐱 Ajude os Gatos!")
            st.image("https://jpimg.com.br/uploads/2025/01/10-curiosidades-sobre-os-filhotes-de-gato.jpg", caption="Um lindo gatinho")
            st.write(
                "Os gatos são animais independentes, curiosos e carismáticos. "
                "Muitos estão em abrigos esperando um lar amoroso. "
                "Você pode ajudar doando ração, medicamentos ou oferecendo adoção responsável."
            )
            st.video("https://www.youtube.com/watch?v=5dsGWM5XGdg")
            st.link_button("🐱 Quero ajudar gatos", "https://catland.org.br")
        elif selection == "Cachorro":
            st.header("🐶 Ajude os Cachorros!")
            st.image("https://placedog.net/500/300?id=1", caption="Um cachorro fofinho")
            st.write(
                "Os cachorros são companheiros leais e adoram brincar. "
                "Infelizmente, muitos sofrem abandono. "
                "Você pode ajudar com doações, lar temporário ou apadrinhando um cãozinho."
            )
            st.video("https://www.youtube.com/watch?v=V4LnorVVxfw")
            st.link_button("🐶 Quero ajudar cachorros", "https://institutocaramelo.org")
        elif selection == "Furão":
            st.header("🦦 Ajude os Furões!")
            st.image("https://wallpapers.com/images/high/cute-ferret-pictures-x3yuxlm7zsaeinnf.webp", caption="Um furão curioso")
            st.write(
                "Furões são brincalhões e cheios de energia, mas também precisam de cuidados especiais. "
                "Procure sempre criadores e protetores responsáveis. "
                "Ajude divulgando informações corretas sobre sua criação."
            )
            st.video("https://youtu.be/ZBoz2mitPiY?si=SrD6f2zl3bTmVV-K")
            st.link_button(
                "🦦 Saiba mais sobre furões",
                "https://reviverestore-org.translate.goog/projects/black-footed-ferret/?_x_tr_sl=en&_x_tr_tl=pt&_x_tr_hl=pt&_x_tr_pto=sge"
            )

    st.divider()
    st.subheader("💡 Como você pode ajudar em geral:")
    st.markdown(
        "- Adote um animal em vez de comprar.\n"
        "- Doe ração, medicamentos ou cobertores.\n"
        "- Seja voluntário em abrigos.\n"
        "- Apoie campanhas de castração."
    )

# -------------------- ABA DE CADASTRO --------------------
with aba_cadastro:
    st.header("📋 Coloque seu Pet para Adoção")
    especie_opcao = st.selectbox("Espécie", ["Gato", "Cachorro", "Furão", "Outro"])

    with st.form("form_adocao"):
        nome_pet = st.text_input("Nome do pet")
        if especie_opcao == "Outro":
            especie = st.text_input("Digite a espécie do pet")
        else:
            especie = especie_opcao

        idade = st.number_input("Idade do pet (anos)", min_value=0, max_value=30, step=1)
        descricao = st.text_area("Descrição (temperamento, cuidados especiais, etc.)")
        contato = st.text_input("Seu telefone ou e-mail para contato")
        foto = st.file_uploader("Foto do pet", type=["jpg", "jpeg", "png"])

        enviar = st.form_submit_button("📨 Enviar para adoção")

        if enviar:
            if nome_pet.strip() == "" or especie.strip() == "":
                st.error("⚠️ Por favor, preencha nome e espécie do pet.")
            elif foto is None:
                st.error("⚠️ Por favor, envie uma foto do pet.")
            else:
                st.session_state.pets_para_adocao.append({
                    "nome": nome_pet,
                    "especie": especie,
                    "idade": idade,
                    "descricao": descricao,
                    "contato": contato,
                    "foto": foto
                })
                st.success(f"✅ Pet {nome_pet} ({especie}) cadastrado para adoção!")

# -------------------- ABA DE VISUALIZAÇÃO --------------------
with aba_ver:
    st.header("🐾 Pets disponíveis para adoção")

    pets = st.session_state.pets_para_adocao
    if not pets:
        st.info("Nenhum pet disponível no momento. Cadastre um pet na aba anterior!")
    else:
        num_cols = 3
        cols = st.columns(num_cols)

        for idx, pet in enumerate(pets):
            col = cols[idx % num_cols]
            with col:
                st.image(pet["foto"], caption=pet["nome"])
                st.subheader(f"{pet['nome']} ({pet['especie']})")
                st.write(f"Idade: {pet['idade']} anos")
                st.write(pet['descricao'])

                if st.button(f"Adotar {pet['nome']}", key=idx):
                    # Armazena o nome do pet adotado e marca para mostrar balões
                    st.session_state.pet_adotado = pet['nome']
                    st.session_state.total_adotados += 1
                    # Remove o pet da lista
                    st.session_state.pets_para_adocao.pop(idx)
                    # Marca para mostrar balões na próxima renderização
                    st.session_state.mostrar_baloes = True
                    # Recarrega a página
                    st.rerun()