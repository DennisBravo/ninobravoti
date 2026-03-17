"""
base_conhecimento.py — Base de conhecimento técnica do Nino
Estrutura: problema → palavras-chave, perguntas de diagnóstico, soluções, categoria
"""

BASE_CONHECIMENTO = {

    # ══════════════════════════════════════
    # OUTLOOK / EMAIL
    # ══════════════════════════════════════

    "outlook não abre": {
        "categoria": "outlook",
        "palavras_chave": ["outlook não abre", "outlook travado", "outlook não inicia", "outlook fecha sozinho"],
        "perguntas": [
            "Ao abrir o Outlook aparece alguma mensagem de erro?",
            "Você consegue abrir o Outlook em modo seguro? (Win+R → outlook.exe /safe)",
            "O problema começou após alguma atualização ou instalação recente?"
        ],
        "solucoes": [
            "Abra o Outlook em modo seguro: Win+R → digite outlook.exe /safe → Enter",
            "Desative complementos: Arquivo → Opções → Suplementos → Gerenciar → Desativar todos",
            "Repare o perfil: Painel de Controle → Email → Mostrar Perfis → Reparar",
            "Repare o Office: Painel de Controle → Programas → Microsoft 365 → Alterar → Reparo Online",
            "Exclua o arquivo de configuração: %appdata%\\Microsoft\\Outlook → delete o arquivo .ost e recrie o perfil"
        ]
    },

    "outlook lento": {
        "categoria": "outlook",
        "palavras_chave": ["outlook lento", "outlook demora", "outlook travando", "email lento"],
        "perguntas": [
            "O Outlook é lento ao abrir ou durante o uso?",
            "Quantos e-mails você tem na caixa de entrada aproximadamente?",
            "Você usa pasta PST local ou apenas Exchange/365?"
        ],
        "solucoes": [
            "Arquive e-mails antigos: Arquivo → Ferramentas de Limpeza → Arquivar",
            "Esvazie a pasta Itens Excluídos e Lixo Eletrônico",
            "Desative complementos desnecessários: Arquivo → Opções → Suplementos",
            "Desative o modo cache se a conexão for boa: Arquivo → Configurações de Conta → Email → Modo Cache",
            "Compacte o arquivo PST se usar: Arquivo → Configurações de Conta → Arquivo de Dados → Configurações → Compactar"
        ]
    },

    "não recebo emails": {
        "categoria": "outlook",
        "palavras_chave": ["não recebo email", "email não chega", "e-mail sumiu", "caixa vazia"],
        "perguntas": [
            "Você consegue enviar e-mails normalmente?",
            "Os e-mails estão chegando na pasta Spam ou Lixo Eletrônico?",
            "O problema é com todos os remetentes ou apenas um específico?"
        ],
        "solucoes": [
            "Verifique a pasta Spam/Lixo Eletrônico",
            "Verifique regras de caixa de entrada: Arquivo → Gerenciar Regras e Alertas",
            "Confira se a caixa não está cheia: Arquivo → Ferramentas de Limpeza",
            "Acesse pelo webmail (outlook.office.com) para confirmar se o problema é local",
            "Verifique se o remetente não está bloqueado: Início → Lixo Eletrônico → Opções → Remetentes Bloqueados"
        ]
    },

    "outlook pede senha sempre": {
        "categoria": "outlook",
        "palavras_chave": ["outlook pedindo senha", "senha outlook toda hora", "autenticação outlook", "login outlook repetindo"],
        "perguntas": [
            "Está pedindo senha a todo momento ou apenas uma vez?",
            "Você alterou a senha recentemente no portal Microsoft 365?",
            "Aparece alguma mensagem de erro específica ao autenticar?"
        ],
        "solucoes": [
            "Confirme se a senha está correta acessando portal.office.com no navegador",
            "Remova credenciais antigas: Gerenciador de Credenciais do Windows → Credenciais do Windows → remova entradas do Office/Outlook",
            "Reconecte a conta: Arquivo → Configurações de Conta → remova e adicione novamente",
            "Se MFA ativo: gere senha de aplicativo em aka.ms/mysecurityinfo",
            "Habilite autenticação moderna se estiver desativada (requer admin)"
        ]
    },

    "email enviado como outro remetente": {
        "categoria": "outlook",
        "palavras_chave": ["enviar como", "remetente errado", "email sai de outro endereço"],
        "perguntas": [
            "Você tem permissão 'Enviar Como' configurada para outra conta?",
            "Em qual conta de e-mail o problema acontece?"
        ],
        "solucoes": [
            "Verifique o campo 'De' ao compor o e-mail — clique em 'De' para selecionar o remetente correto",
            "Se o campo 'De' não aparecer: Opções → Do → ativar",
            "Remova delegações desnecessárias: Arquivo → Configurações de Conta → Acesso de Delegado"
        ]
    },

    "assinatura outlook sumiu": {
        "categoria": "outlook",
        "palavras_chave": ["assinatura sumiu", "assinatura desapareceu", "sem assinatura email"],
        "perguntas": [
            "A assinatura sumiu apenas neste computador ou em todos?",
            "Você reinstalou o Office recentemente?"
        ],
        "solucoes": [
            "Recrie a assinatura: Arquivo → Opções → Email → Assinaturas",
            "Se usar assinatura corporativa centralizada: contate o administrador de TI",
            "Arquivos de assinatura ficam em: %appdata%\\Microsoft\\Signatures — verifique se ainda existem"
        ]
    },

    # ══════════════════════════════════════
    # MICROSOFT TEAMS
    # ══════════════════════════════════════

    "teams não abre": {
        "categoria": "teams",
        "palavras_chave": ["teams não abre", "teams travado", "teams não inicia", "teams carregando"],
        "perguntas": [
            "O Teams trava na tela de carregamento ou nem abre?",
            "Você consegue acessar o Teams pelo navegador (teams.microsoft.com)?",
            "Quando começou o problema?"
        ],
        "solucoes": [
            "Feche o Teams completamente (inclusive na bandeja do sistema → botão direito → Sair)",
            "Limpe o cache: Win+R → %appdata%\\Microsoft\\Teams → delete a pasta 'Cache'",
            "Reinicie o computador e abra o Teams novamente",
            "Desinstale e reinstale pelo portal office.com",
            "Use o Teams Web como alternativa: teams.microsoft.com"
        ]
    },

    "teams sem som": {
        "categoria": "teams",
        "palavras_chave": ["teams sem áudio", "não ouve no teams", "teams sem som", "áudio teams"],
        "perguntas": [
            "O problema de áudio é só no Teams ou em todo o computador?",
            "Você está usando fone, caixa de som ou alto-falante do notebook?",
            "Nas configurações do Teams, qual dispositivo de áudio está selecionado?"
        ],
        "solucoes": [
            "No Teams: foto de perfil → Configurações → Dispositivos → selecione o dispositivo correto",
            "Verifique se o dispositivo está como padrão no Windows: Configurações → Som",
            "Teste o áudio: Teams → Configurações → Dispositivos → Fazer teste de chamada",
            "Verifique permissão de microfone: Configurações Windows → Privacidade → Microfone → Teams ativado",
            "Reinstale o driver de áudio pelo Gerenciador de Dispositivos"
        ]
    },

    "câmera não funciona teams": {
        "categoria": "teams",
        "palavras_chave": ["câmera teams", "camera teams", "webcam teams", "video teams não funciona"],
        "perguntas": [
            "A câmera funciona em outros aplicativos (ex: câmera do Windows)?",
            "Aparece alguma mensagem de erro ao ativar a câmera?",
            "A câmera aparece nas configurações do Teams?"
        ],
        "solucoes": [
            "Verifique permissão: Configurações Windows → Privacidade → Câmera → Teams ativado",
            "No Teams: Configurações → Dispositivos → selecione a câmera correta",
            "Feche outros apps que possam estar usando a câmera (Zoom, Meet, etc.)",
            "Reinstale o driver da câmera no Gerenciador de Dispositivos",
            "Teste a câmera pelo app nativo: Menu Iniciar → Câmera"
        ]
    },

    "teams não entra na reunião": {
        "categoria": "teams",
        "palavras_chave": ["não consigo entrar reunião teams", "erro ao entrar reunião", "reunião teams não abre"],
        "perguntas": [
            "Aparece alguma mensagem de erro ao tentar entrar?",
            "Você está logado com a conta correta no Teams?",
            "A reunião exige autenticação ou é pública?"
        ],
        "solucoes": [
            "Tente entrar pelo navegador: abra o link da reunião no Edge ou Chrome",
            "Verifique se está logado com a conta correta: foto de perfil → conta",
            "Limpe o cache do Teams: %appdata%\\Microsoft\\Teams → pasta Cache",
            "Se pedir senha ou for bloqueado: contate o organizador da reunião",
            "Atualize o Teams para a versão mais recente"
        ]
    },

    "teams mensagens não carregam": {
        "categoria": "teams",
        "palavras_chave": ["mensagens teams não aparecem", "chat teams vazio", "teams não carrega mensagens"],
        "perguntas": [
            "O problema é em todos os chats ou apenas em um específico?",
            "Você consegue enviar mensagens mesmo sem ver as anteriores?"
        ],
        "solucoes": [
            "Limpe o cache do Teams: %appdata%\\Microsoft\\Teams → delete pasta Cache",
            "Saia e entre novamente na conta do Teams",
            "Verifique a conexão com a internet",
            "Acesse via Teams Web para confirmar se o problema é local"
        ]
    },

    # ══════════════════════════════════════
    # SHAREPOINT
    # ══════════════════════════════════════

    "sharepoint sem acesso": {
        "categoria": "sharepoint",
        "palavras_chave": ["sharepoint acesso negado", "sem permissão sharepoint", "não consigo acessar sharepoint"],
        "perguntas": [
            "Qual mensagem de erro aparece ao acessar?",
            "Você tinha acesso antes ou nunca teve acesso a esse site?",
            "É um site de equipe, biblioteca de documentos ou pasta específica?"
        ],
        "solucoes": [
            "Confirme qual conta está logada: canto superior direito do SharePoint",
            "Na página de erro, clique em 'Solicitar Acesso' se disponível",
            "Verifique se não está usando conta pessoal Microsoft em vez da corporativa",
            "Limpe o cache do navegador: Ctrl+Shift+Del",
            "O administrador do site precisa conceder permissão — informe o link e sua necessidade"
        ]
    },

    "arquivo sharepoint não abre": {
        "categoria": "sharepoint",
        "palavras_chave": ["arquivo sharepoint não abre", "documento sharepoint erro", "sharepoint arquivo travado"],
        "perguntas": [
            "O arquivo é do Word, Excel, PowerPoint ou outro formato?",
            "Aparece mensagem de 'arquivo bloqueado para edição'?",
            "Você está tentando abrir pelo navegador ou pelo aplicativo?"
        ],
        "solucoes": [
            "Se bloqueado para edição: verifique quem está com o arquivo aberto",
            "Abra pelo aplicativo desktop: no SharePoint → clique nos três pontos → Abrir no aplicativo",
            "Para desbloquear: aguarde o outro usuário fechar ou contate o administrador",
            "Verifique se o arquivo não está com check-out ativo: três pontos → Desfazer check-out",
            "Se arquivo corrompido: verifique versões anteriores → Histórico de Versão"
        ]
    },

    "sharepoint lento": {
        "categoria": "sharepoint",
        "palavras_chave": ["sharepoint lento", "sharepoint demora carregar", "site sharepoint devagar"],
        "perguntas": [
            "O SharePoint é lento em todos os navegadores ou apenas em um?",
            "Você está acessando da empresa ou de casa (VPN)?"
        ],
        "solucoes": [
            "Limpe o cache e cookies do navegador: Ctrl+Shift+Del",
            "Tente no Edge ou Chrome (browsers mais compatíveis com SharePoint)",
            "Desative extensões do navegador temporariamente",
            "Se estiver na VPN, tente acessar direto pela internet se a política permitir",
            "Verifique a velocidade da internet em speedtest.net"
        ]
    },

    # ══════════════════════════════════════
    # ONEDRIVE
    # ══════════════════════════════════════

    "onedrive não sincroniza": {
        "categoria": "onedrive",
        "palavras_chave": ["onedrive não sincroniza", "onedrive parado", "arquivos não sobem onedrive"],
        "perguntas": [
            "O ícone do OneDrive na bandeja mostra X vermelho, seta ou nuvem com risco?",
            "É um arquivo específico ou todos os arquivos estão com problema?",
            "Qual é o espaço disponível no seu OneDrive?"
        ],
        "solucoes": [
            "Clique no ícone do OneDrive → Ajuda e Configurações → Pausar sincronização → Retomar",
            "Verifique nomes de arquivos inválidos (caracteres: # % & * : < > ? / \\)",
            "Reinicie o OneDrive: ícone → Fechar OneDrive → abra pelo Menu Iniciar",
            "Verifique a cota em onedrive.live.com",
            "Desvincule e vincule novamente: ícone → Configurações → Conta → Desvincular"
        ]
    },

    "onedrive arquivos sumidos": {
        "categoria": "onedrive",
        "palavras_chave": ["arquivo sumiu onedrive", "pasta desapareceu onedrive", "arquivo deletado onedrive"],
        "perguntas": [
            "Você deletou o arquivo ou ele sumiu sozinho?",
            "Outros usuários têm acesso a essa pasta?"
        ],
        "solucoes": [
            "Verifique a Lixeira do OneDrive: acesse onedrive.live.com → Lixeira",
            "Arquivos ficam na lixeira por 93 dias",
            "Verifique versões anteriores: clique com botão direito no arquivo → Histórico de Versão",
            "Se a pasta era compartilhada: verifique com o dono se houve remoção",
            "Contate o administrador Microsoft 365 para restauração via admin center"
        ]
    },

    # ══════════════════════════════════════
    # VPN
    # ══════════════════════════════════════

    "vpn não conecta": {
        "categoria": "vpn",
        "palavras_chave": ["vpn não conecta", "vpn erro", "vpn caiu", "não consigo conectar vpn"],
        "perguntas": [
            "Qual mensagem de erro aparece ao tentar conectar?",
            "Você está em casa, hotel ou outra rede externa?",
            "A VPN funcionava antes nessa mesma rede?"
        ],
        "solucoes": [
            "Verifique se há internet antes de conectar a VPN",
            "Feche o cliente VPN completamente e abra novamente",
            "Se alterou a senha corporativa recentemente: atualize na VPN também",
            "Desative antivírus/firewall pessoal temporariamente e tente conectar",
            "Se GlobalProtect: verifique o serviço em services.msc → Palo Alto GlobalProtect"
        ]
    },

    "vpn lenta": {
        "categoria": "vpn",
        "palavras_chave": ["vpn lenta", "internet lenta com vpn", "vpn deixa computador lento"],
        "perguntas": [
            "A internet é lenta só com a VPN ou também sem ela?",
            "Em qual região/servidor VPN você está conectado?"
        ],
        "solucoes": [
            "Teste a velocidade com e sem VPN em speedtest.net",
            "Tente conectar em outro servidor VPN (mais próximo geograficamente)",
            "Feche aplicativos que consomem banda (streaming, backup em nuvem)",
            "Verifique se o roteador doméstico está atualizado",
            "Contate o TI — pode ser necessário ajustar o split tunneling"
        ]
    },

    "vpn desconecta sozinha": {
        "categoria": "vpn",
        "palavras_chave": ["vpn cai sozinha", "vpn desconecta", "vpn não mantém conexão"],
        "perguntas": [
            "Com que frequência a VPN desconecta? A cada quantos minutos?",
            "Acontece em qualquer rede ou apenas em algumas?"
        ],
        "solucoes": [
            "Verifique se o computador está indo para suspensão: Configurações → Energia → nunca suspender",
            "Nas configurações do cliente VPN: ative reconexão automática se disponível",
            "Verifique se o roteador tem firewall bloqueando conexões longas",
            "Atualize o cliente VPN para a versão mais recente",
            "Contate o TI para revisar políticas de timeout da VPN"
        ]
    },

    # ══════════════════════════════════════
    # IMPRESSORA
    # ══════════════════════════════════════

    "impressora não imprime": {
        "categoria": "impressora",
        "palavras_chave": ["impressora não imprime", "impressora parada", "documento na fila impressão"],
        "perguntas": [
            "Aparece alguma mensagem de erro na fila de impressão?",
            "A impressora está ligada e com luzes normais?",
            "O problema é com todos os documentos ou um específico?"
        ],
        "solucoes": [
            "Verifique a fila: botão direito na impressora → Ver o que está sendo impresso → cancele todos",
            "Reinicie o spooler: Win+R → services.msc → Print Spooler → Reiniciar",
            "Desligue a impressora, aguarde 30s e ligue novamente",
            "Remova e reinstale o driver pelo Gerenciador de Dispositivos",
            "Teste imprimir de outro computador para identificar se é problema local ou na impressora"
        ]
    },

    "impressora offline": {
        "categoria": "impressora",
        "palavras_chave": ["impressora offline", "impressora aparece offline", "impressora desconectada"],
        "perguntas": [
            "A impressora é conectada por cabo USB, rede ou Wi-Fi?",
            "Outros computadores conseguem imprimir nela?"
        ],
        "solucoes": [
            "Botão direito na impressora → Ver o que está sendo impresso → Impressora → Desmarcar 'Usar impressora offline'",
            "Desligue e ligue a impressora novamente",
            "Se for de rede: verifique se o IP da impressora mudou — reimprima a página de configuração",
            "Remova e adicione a impressora novamente nas configurações",
            "Verifique o cabo ou reconecte ao Wi-Fi da impressora"
        ]
    },

    "impressora imprime borrado": {
        "categoria": "impressora",
        "palavras_chave": ["impressão borrada", "toner fraco", "impressão com manchas", "qualidade impressão ruim"],
        "perguntas": [
            "É impressora laser ou jato de tinta?",
            "O problema é em toda a página ou apenas em partes?"
        ],
        "solucoes": [
            "Para laser: agite o cartucho de toner suavemente para redistribuir o pó",
            "Para jato de tinta: execute a limpeza de cabeçote nas propriedades da impressora",
            "Verifique o nível de tinta/toner nas propriedades da impressora",
            "Substitua o cartucho/toner se estiver no fim",
            "Execute o alinhamento de cabeçote nas propriedades de manutenção"
        ]
    },

    # ══════════════════════════════════════
    # HARDWARE / NOTEBOOK
    # ══════════════════════════════════════

    "notebook lento": {
        "categoria": "hardware",
        "palavras_chave": ["computador lento", "notebook lento", "pc travando", "sistema lento"],
        "perguntas": [
            "O computador é lento desde que liga ou piora com o tempo de uso?",
            "Quanto espaço livre há no disco? (verificar no Explorador de Arquivos)",
            "O problema acontece em todos os programas ou apenas na internet?"
        ],
        "solucoes": [
            "Reinicie o computador completamente (não apenas suspender)",
            "Ctrl+Shift+Esc → aba Inicialização → desative programas desnecessários",
            "Verifique o espaço em disco: deve ter pelo menos 15% livre",
            "Execute Limpeza de Disco: Menu Iniciar → 'limpeza de disco'",
            "Verifique por vírus com o Windows Defender"
        ]
    },

    "notebook não liga": {
        "categoria": "hardware",
        "palavras_chave": ["notebook não liga", "computador não liga", "pc não liga", "não inicializa"],
        "perguntas": [
            "Ao pressionar o botão ligar, alguma luz acende ou você ouve algum som?",
            "O notebook estava funcionando normalmente antes?",
            "Já tentou conectar na tomada diretamente sem extensão?"
        ],
        "solucoes": [
            "Conecte o carregador original e aguarde 10 minutos antes de tentar ligar",
            "Pressione e segure o botão de ligar por 15 segundos",
            "Se bateria removível: retire, pressione ligar 10s sem bateria, recoloque e tente",
            "Conecte um monitor externo — pode ser falha apenas na tela",
            "Se nada funcionar: falha de hardware — necessário suporte presencial"
        ]
    },

    "tela azul bsod": {
        "categoria": "hardware",
        "palavras_chave": ["tela azul", "bsod", "blue screen", "erro crítico windows", "sistema reiniciou"],
        "perguntas": [
            "Qual código de erro apareceu na tela azul?",
            "A tela azul aparece ao iniciar o Windows ou durante o uso?",
            "Aconteceu após atualização ou instalação de programa?"
        ],
        "solucoes": [
            "Anote o código de erro (ex: KERNEL_SECURITY_CHECK_FAILURE)",
            "Inicie em Modo Seguro: F8 durante o boot",
            "Execute no Prompt como admin: sfc /scannow",
            "Depois execute: DISM /Online /Cleanup-Image /RestoreHealth",
            "Se recorrente após atualização: desinstale a atualização pelo Windows Update"
        ]
    },

    "notebook superaquecendo": {
        "categoria": "hardware",
        "palavras_chave": ["notebook quente", "superaquecimento", "ventilador barulhento", "fan barulho", "computador esquentando"],
        "perguntas": [
            "O notebook fica quente o tempo todo ou apenas ao usar programas pesados?",
            "O ventilador está fazendo barulho excessivo?"
        ],
        "solucoes": [
            "Verifique se as saídas de ar não estão bloqueadas (use em superfície dura)",
            "Feche programas desnecessários: Ctrl+Shift+Esc → encerre processos pesados",
            "Use o notebook em superfície rígida, nunca em cama ou travesseiro",
            "Verifique o plano de energia: prefira 'Balanceado' em vez de 'Alto Desempenho'",
            "Limpeza interna de poeira: requer suporte técnico presencial"
        ]
    },

    "bateria não carrega": {
        "categoria": "hardware",
        "palavras_chave": ["bateria não carrega", "notebook não carrega", "bateria parada", "carregador não funciona"],
        "perguntas": [
            "O ícone de bateria mostra 'Conectado, não carregando' ou fica em 0%?",
            "O carregador original está sendo usado?",
            "A bateria chegou a alguma porcentagem ou está completamente morta?"
        ],
        "solucoes": [
            "Tente outro carregador original compatível",
            "Desligue o notebook completamente, conecte o carregador e aguarde 30 minutos antes de ligar",
            "Remova a bateria (se removível), conecte apenas o carregador e ligue",
            "Atualize o driver da bateria: Gerenciador de Dispositivos → Baterias → Desinstalar e reiniciar",
            "Se mostrar 'Considere substituir a bateria': bateria desgastada — troca necessária"
        ]
    },

    "teclado não funciona": {
        "categoria": "hardware",
        "palavras_chave": ["teclado não digita", "teclado parou", "tecla não funciona", "teclado com defeito"],
        "perguntas": [
            "É o teclado do próprio notebook ou um teclado externo?",
            "Todas as teclas não funcionam ou apenas algumas?",
            "Acontece em todos os programas ou apenas em um?"
        ],
        "solucoes": [
            "Reinicie o computador — problema pode ser temporário",
            "Se teclado externo USB: desconecte e reconecte em outra porta USB",
            "Verifique se a tecla NumLock ou FnLock está ativada",
            "Atualize o driver: Gerenciador de Dispositivos → Teclados → Atualizar driver",
            "Teste com teclado virtual: Menu Iniciar → Teclado Virtual"
        ]
    },

    "mouse não funciona": {
        "categoria": "hardware",
        "palavras_chave": ["mouse não funciona", "mouse travado", "cursor não move", "touchpad parou"],
        "perguntas": [
            "É mouse USB, Bluetooth ou o touchpad do notebook?",
            "O cursor aparece na tela ou sumiu completamente?"
        ],
        "solucoes": [
            "Se USB: desconecte e reconecte em outra porta",
            "Se Bluetooth: remova o dispositivo e pareie novamente",
            "Para touchpad: verifique se não foi desativado acidentalmente (geralmente Fn + tecla de touchpad)",
            "Reinicie o computador",
            "Atualize o driver: Gerenciador de Dispositivos → Mouses → Atualizar driver"
        ]
    },

    "monitor sem sinal": {
        "categoria": "hardware",
        "palavras_chave": ["monitor sem sinal", "tela preta monitor", "sem imagem monitor", "monitor não liga"],
        "perguntas": [
            "O monitor mostra 'Sem sinal' ou está completamente apagado?",
            "É o monitor do notebook ou um monitor externo?",
            "O computador parece estar ligado (luzes, sons)?"
        ],
        "solucoes": [
            "Verifique o cabo de vídeo (HDMI, DisplayPort ou VGA) — desconecte e reconecte",
            "Teste com outro cabo de vídeo",
            "Pressione Win+P para alternar modos de exibição",
            "Conecte um monitor diferente para identificar se é o monitor ou o computador",
            "Reinicie segurando o botão de ligar por 10 segundos"
        ]
    },

    # ══════════════════════════════════════
    # WINDOWS / SISTEMA OPERACIONAL
    # ══════════════════════════════════════

    "windows update falhando": {
        "categoria": "windows",
        "palavras_chave": ["atualização windows falhou", "windows update erro", "atualização não instala", "update travado"],
        "perguntas": [
            "Qual código de erro aparece na atualização?",
            "Há quanto tempo as atualizações estão falhando?"
        ],
        "solucoes": [
            "Execute o solucionador de problemas: Configurações → Windows Update → Solucionar problemas",
            "Limpe o cache do Windows Update: pare o serviço wuauserv, delete C:\\Windows\\SoftwareDistribution, reinicie o serviço",
            "Execute no Prompt admin: DISM /Online /Cleanup-Image /RestoreHealth",
            "Depois: sfc /scannow",
            "Se persistir: atualize manualmente pelo Catálogo do Microsoft Update"
        ]
    },

    "windows lento na inicialização": {
        "categoria": "windows",
        "palavras_chave": ["windows demora iniciar", "boot lento", "windows lento para ligar", "inicialização demorada"],
        "perguntas": [
            "Quando começou a ficar lento para iniciar?",
            "Quantos programas abrem automaticamente ao iniciar?"
        ],
        "solucoes": [
            "Desative programas na inicialização: Ctrl+Shift+Esc → aba Inicialização → desative os desnecessários",
            "Ative o Fast Startup: Painel de Controle → Opções de Energia → Escolher a função dos botões → ligar Inicialização Rápida",
            "Verifique saúde do disco: Prompt admin → chkdsk C: /f",
            "Se HD mecânico: considere migração para SSD (melhora dramática)",
            "Verifique vírus com Windows Defender"
        ]
    },

    "programa não instala windows": {
        "categoria": "windows",
        "palavras_chave": ["programa não instala", "instalação falhou", "erro ao instalar programa", "setup falhou"],
        "perguntas": [
            "Qual programa está tentando instalar e qual erro aparece?",
            "Você tem permissão de administrador no computador?"
        ],
        "solucoes": [
            "Clique com botão direito no instalador → Executar como administrador",
            "Verifique se o antivírus está bloqueando a instalação — desative temporariamente",
            "Verifique se há espaço suficiente em disco",
            "Baixe novamente o instalador — pode estar corrompido",
            "Verifique os requisitos mínimos do sistema para o programa"
        ]
    },

    "windows não ativa": {
        "categoria": "windows",
        "palavras_chave": ["windows não ativado", "ativar windows", "licença windows expirou", "marca d'água windows"],
        "perguntas": [
            "O Windows mostra mensagem de 'Ativar o Windows' ou 'Licença expirada'?",
            "O computador é corporativo (parte do domínio da empresa)?"
        ],
        "solucoes": [
            "Se corporativo: a ativação é gerenciada pelo servidor KMS — conecte à rede da empresa ou VPN",
            "Verifique o status: Configurações → Sistema → Ativação",
            "Execute no Prompt admin: slmgr /ato — força a ativação via KMS",
            "Se licença OEM: chave está na BIOS — reinstale o Windows que ativa automaticamente",
            "Contate o TI para verificar o licenciamento"
        ]
    },

    # ══════════════════════════════════════
    # INTERNET / REDE
    # ══════════════════════════════════════

    "sem internet": {
        "categoria": "internet",
        "palavras_chave": ["sem internet", "internet caiu", "sem conexão", "rede não funciona", "wifi não conecta"],
        "perguntas": [
            "O problema é só no seu computador ou em outros dispositivos também?",
            "O roteador está com as luzes normais?",
            "Você está em Wi-Fi ou cabo?"
        ],
        "solucoes": [
            "Reinicie o roteador: desligue da tomada, aguarde 30s, ligue novamente",
            "Configurações → Rede e Internet → Solução de Problemas",
            "Prompt admin → ipconfig /flushdns e depois netsh winsock reset → reinicie",
            "Se Wi-Fi: esqueça a rede e conecte novamente com a senha",
            "Se cabo: troque o cabo ou teste em outra porta do roteador"
        ]
    },

    "internet lenta": {
        "categoria": "internet",
        "palavras_chave": ["internet lenta", "navegação lenta", "site demora carregar", "streaming travando"],
        "perguntas": [
            "A internet é lenta em todos os dispositivos ou apenas no seu computador?",
            "Qual a velocidade no speedtest.net agora? Qual é o plano contratado?"
        ],
        "solucoes": [
            "Teste em speedtest.net e compare com a velocidade contratada",
            "Se Wi-Fi: aproxime-se do roteador ou use cabo",
            "Feche abas, downloads e atualizações em segundo plano",
            "Troque o DNS: Configurações de rede → propriedades → use 8.8.8.8 e 8.8.4.4 (Google)",
            "Reinicie o roteador"
        ]
    },

    "wifi não aparece": {
        "categoria": "internet",
        "palavras_chave": ["wifi sumiu", "rede wifi não aparece", "sem redes disponíveis", "adaptador wifi"],
        "perguntas": [
            "O ícone de Wi-Fi aparece na barra de tarefas ou desapareceu completamente?",
            "O modo avião está ativado?"
        ],
        "solucoes": [
            "Verifique o modo avião: clique no ícone de rede → desative o modo avião",
            "Pressione a tecla de Wi-Fi no teclado (geralmente Fn + tecla com símbolo Wi-Fi)",
            "Atualize o driver Wi-Fi: Gerenciador de Dispositivos → Adaptadores de Rede → Atualizar driver",
            "Desative e reative o adaptador: Gerenciador de Dispositivos → botão direito → Desabilitar/Habilitar",
            "Se sumir completamente: execute sfc /scannow no Prompt admin"
        ]
    },

    # ══════════════════════════════════════
    # SENHA / ACESSO / MFA
    # ══════════════════════════════════════

    "esqueci minha senha": {
        "categoria": "acesso",
        "palavras_chave": ["esqueci senha", "senha incorreta", "não consigo logar", "senha expirou"],
        "perguntas": [
            "É a senha do Windows, do e-mail corporativo ou de outro sistema?",
            "Você tem acesso ao celular cadastrado para recuperação?",
            "A senha expirou ou você simplesmente esqueceu?"
        ],
        "solucoes": [
            "Reset Microsoft 365: acesse aka.ms/sspr com seu e-mail corporativo",
            "Se não tiver SSPR: contate o administrador de TI para reset via Azure AD",
            "Senha do Windows em domínio: pressione Ctrl+Alt+Del → Alterar senha",
            "Após resetar: atualize em TODOS os dispositivos (Teams, Outlook mobile, OneDrive)"
        ]
    },

    "conta bloqueada": {
        "categoria": "acesso",
        "palavras_chave": ["conta bloqueada", "usuário bloqueado", "muitas tentativas senha", "conta desabilitada"],
        "perguntas": [
            "Aparece mensagem de 'conta bloqueada' ou 'credenciais incorretas'?",
            "Você tentou fazer login várias vezes com senha errada?"
        ],
        "solucoes": [
            "Aguarde 15-30 minutos e tente novamente (desbloqueio automático em muitas políticas)",
            "Contate o administrador de TI para desbloquear manualmente no Active Directory",
            "Verifique se não há dispositivo com senha antiga tentando logar automaticamente (celular, outro PC)",
            "Após desbloqueio: altere a senha imediatamente"
        ]
    },

    "mfa não funciona": {
        "categoria": "acesso",
        "palavras_chave": ["mfa não funciona", "autenticação dois fatores falhou", "código mfa não chega", "authenticator erro"],
        "perguntas": [
            "O código MFA não chega ou chega mas dá erro ao inserir?",
            "Você trocou de celular recentemente?",
            "Está usando Microsoft Authenticator, SMS ou ligação?"
        ],
        "solucoes": [
            "Acesse aka.ms/mysecurityinfo para gerenciar métodos de autenticação",
            "Se trocou de celular: um administrador precisa resetar o MFA no Azure AD",
            "Verifique se o horário do celular está correto e sincronizado",
            "Se SMS: aguarde até 2 minutos ou solicite reenvio",
            "Use código de backup se tiver cadastrado"
        ]
    },

    "acesso negado pasta rede": {
        "categoria": "acesso",
        "palavras_chave": ["acesso negado pasta", "sem permissão pasta", "não acessa servidor arquivo", "rede compartilhada erro"],
        "perguntas": [
            "Você conseguia acessar essa pasta antes?",
            "Outros colegas conseguem acessar essa mesma pasta?"
        ],
        "solucoes": [
            "Verifique se está conectado à rede correta (VPN se for remoto)",
            "Tente acessar pelo caminho direto: Win+R → \\\\servidor\\pasta",
            "Verifique credenciais salvas: Gerenciador de Credenciais → atualize as credenciais de rede",
            "Contate o administrador para verificar permissões no servidor"
        ]
    },

    # ══════════════════════════════════════
    # MICROSOFT 365 / OFFICE
    # ══════════════════════════════════════

    "office não ativa": {
        "categoria": "microsoft365",
        "palavras_chave": ["office não ativado", "ativar office", "licença office", "office modo somente leitura"],
        "perguntas": [
            "Qual mensagem aparece ao tentar usar o Office?",
            "Você tem uma licença Microsoft 365 atribuída?"
        ],
        "solucoes": [
            "Abra qualquer app Office → Arquivo → Conta → Entrar com a conta corporativa",
            "Verifique a licença em portal.office.com → clique na foto de perfil → Minha conta → Assinaturas",
            "Saia e entre novamente: Arquivo → Conta → Sair → Entrar",
            "Execute o assistente de suporte: aka.ms/SaRA",
            "Contate o administrador para verificar se a licença está atribuída"
        ]
    },

    "word trava ao salvar": {
        "categoria": "microsoft365",
        "palavras_chave": ["word trava", "word congela", "word fecha sozinho", "word não salva"],
        "perguntas": [
            "O Word trava ao salvar localmente, no OneDrive ou no SharePoint?",
            "O arquivo é grande (muitas imagens ou tabelas complexas)?"
        ],
        "solucoes": [
            "Salve como cópia local primeiro: Arquivo → Salvar Como → Este PC",
            "Desative o AutoSalvar temporariamente e salve manualmente",
            "Desative complementos: Arquivo → Opções → Suplementos → Gerenciar COM → desative todos",
            "Repare o Office: Painel de Controle → Microsoft 365 → Alterar → Reparo Online",
            "Tente abrir o arquivo em outro computador para confirmar se é o arquivo ou a instalação"
        ]
    },

    "excel arquivo corrompido": {
        "categoria": "microsoft365",
        "palavras_chave": ["excel corrompido", "excel não abre arquivo", "planilha corrompida", "arquivo excel com erro"],
        "perguntas": [
            "O arquivo abre com erro ou não abre de forma alguma?",
            "Você tem uma versão anterior salva ou backup?"
        ],
        "solucoes": [
            "Tente abrir e reparar: Excel → Arquivo → Abrir → selecione o arquivo → seta ao lado de Abrir → Abrir e Reparar",
            "Verifique versões anteriores: botão direito no arquivo → Propriedades → Versões Anteriores",
            "Se no OneDrive/SharePoint: Histórico de Versão",
            "Tente abrir no Google Planilhas como alternativa",
            "Use o recuperador de arquivos do Office: aka.ms/SaRA"
        ]
    },

    # ══════════════════════════════════════
    # SEGURANÇA
    # ══════════════════════════════════════

    "suspeita de vírus": {
        "categoria": "segurança",
        "palavras_chave": ["vírus", "malware", "computador infectado", "pop-up estranho", "ransomware", "arquivo suspeito"],
        "perguntas": [
            "O que está acontecendo de estranho? Pop-ups, lentidão repentina, arquivos criptografados?",
            "Você abriu algum link ou arquivo suspeito recentemente?"
        ],
        "solucoes": [
            "IMEDIATAMENTE: desconecte o computador da rede (cabo ou Wi-Fi)",
            "Contate o TI urgentemente antes de fazer qualquer outra coisa",
            "Não desligue o computador — pode ajudar a preservar evidências",
            "Não pague nenhum resgate se for ransomware",
            "Execute o Windows Defender OFFLINE (mais poderoso que o scan normal)"
        ]
    },

    "phishing email suspeito": {
        "categoria": "segurança",
        "palavras_chave": ["email suspeito", "phishing", "golpe email", "link suspeito", "cliquei em link falso"],
        "perguntas": [
            "Você clicou em algum link ou baixou algum anexo do e-mail suspeito?",
            "O e-mail pedia sua senha ou dados bancários?"
        ],
        "solucoes": [
            "Se clicou em link: desconecte da rede e notifique o TI imediatamente",
            "Se inseriu sua senha: troque imediatamente em aka.ms/mysecurityinfo",
            "Não clique em nenhum outro link do e-mail",
            "Reporte o e-mail como phishing: botão direito → Reportar → Phishing",
            "Monitore sua conta por acessos suspeitos em aka.ms/mysignins"
        ]
    },

    # ══════════════════════════════════════
    # OUTROS COMUNS
    # ══════════════════════════════════════

    "pendrive não reconhecido": {
        "categoria": "hardware",
        "palavras_chave": ["pendrive não aparece", "usb não reconhece", "dispositivo usb não detectado"],
        "perguntas": [
            "O pendrive aparece no Gerenciador de Dispositivos?",
            "Funciona em outro computador?"
        ],
        "solucoes": [
            "Tente em outra porta USB",
            "Verifique no Gerenciador de Dispositivos se há erro no dispositivo USB",
            "Gerenciamento de Disco: Win+X → Gerenciamento de Disco — verifique se o pendrive aparece sem letra",
            "Atribua uma letra de unidade se necessário",
            "Se política de TI bloquear USB: contate o administrador"
        ]
    },

    "zoom não funciona": {
        "categoria": "software",
        "palavras_chave": ["zoom não abre", "zoom erro", "zoom sem áudio", "zoom sem câmera"],
        "perguntas": [
            "O problema é ao abrir o Zoom ou durante uma reunião?",
            "É problema de áudio, vídeo ou conexão?"
        ],
        "solucoes": [
            "Atualize o Zoom para a versão mais recente",
            "Verifique permissões: Configurações Windows → Privacidade → Câmera e Microfone → Zoom ativado",
            "Limpe o cache do Zoom: %appdata%\\Zoom → delete a pasta",
            "Teste em zoom.us/test antes da reunião",
            "Desinstale e reinstale o Zoom"
        ]
    },

    "não consigo imprimir pdf": {
        "categoria": "software",
        "palavras_chave": ["pdf não imprime", "imprimir pdf erro", "adobe não imprime"],
        "perguntas": [
            "Qual programa está usando para abrir o PDF?",
            "Outros tipos de documento imprimem normalmente?"
        ],
        "solucoes": [
            "Tente imprimir pelo navegador: abra o PDF no Chrome ou Edge e imprima de lá",
            "Baixe e use o Adobe Acrobat Reader gratuito",
            "Ao imprimir: marque a opção 'Imprimir como imagem' nas propriedades",
            "Salve o PDF novamente com outro nome e tente imprimir",
            "Verifique se o arquivo não está protegido contra impressão"
        ]
    }
}


# ─────────────────────────────────────────
# FUNÇÕES DE BUSCA
# ─────────────────────────────────────────
def buscar_solucao(pergunta_usuario: str) -> dict | None:
    """Retorna o bloco de conhecimento mais relevante."""
    pergunta = pergunta_usuario.lower()

    # Busca por palavras-chave específicas (maior precisão)
    melhor_match = None
    maior_score = 0

    for problema, dados in BASE_CONHECIMENTO.items():
        score = 0
        for palavra in dados.get("palavras_chave", []):
            if palavra in pergunta:
                score += len(palavra.split())  # frases maiores valem mais

        # Fallback: palavras do nome do problema
        palavras_problema = problema.split()
        for p in palavras_problema:
            if len(p) > 3 and p in pergunta:
                score += 1

        if score > maior_score:
            maior_score = score
            melhor_match = (problema, dados)

    if melhor_match and maior_score > 0:
        problema, dados = melhor_match
        return {"problema": problema, **dados}

    return None


def conhecimento_para_prompt() -> str:
    """Gera resumo da base para injetar no SYSTEM_PROMPT."""
    linhas = ["BASE DE CONHECIMENTO BRAVO TI — USE ESTAS INFORMAÇÕES:\n"]
    for problema, dados in BASE_CONHECIMENTO.items():
        linhas.append(f"## {problema.upper()} [{dados.get('categoria','').upper()}]")
        linhas.append("Perguntas de diagnóstico:")
        for p in dados["perguntas"][:2]:  # limita para não explodir o prompt
            linhas.append(f"  - {p}")
        linhas.append("Soluções principais:")
        for s in dados["solucoes"][:3]:
            linhas.append(f"  • {s}")
        linhas.append("")
    return "\n".join(linhas)


def listar_categorias() -> list:
    """Retorna lista de categorias únicas da base."""
    return list(set(d.get("categoria", "outros") for d in BASE_CONHECIMENTO.values()))