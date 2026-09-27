# PWA Construtora Mão de Obra Ltda

Landing page estática para GitHub Pages.

## Executar localmente

Preencha o arquivo `.env`. O WhatsApp deve usar o formato internacional, apenas com números, por exemplo `5512999999999`. Em `CONTACT_INSTAGRAM`, informe somente o usuário, sem `@`.

```powershell
node build.mjs
python -m http.server 8000 -d dist
```

Abra `http://localhost:8000`.

O build aceita as mesmas opções como variáveis de ambiente e dá prioridade a elas sobre o `.env`. Isso permite configurar os dados futuramente no GitHub Actions.

## Contatos disponíveis

- `CONTACT_WHATSAPP_NUMBER`: obrigatório.
- `CONTACT_WHATSAPP_MESSAGE`: mensagem inicial do orçamento.
- `CONTACT_INSTAGRAM`: usuário do Instagram.
- `CONTACT_PHONE`: telefone exibido no site.
- `CONTACT_EMAIL`: e-mail comercial.
- `CONTACT_BUSINESS_HOURS`: horário de atendimento.
- `CONTACT_MAPS_URL`: link HTTPS do Google Maps.

Contatos opcionais vazios não aparecem no site. O arquivo `.env` é local e não é publicado; mantenha o `.env.example` como referência.

## Testes

```powershell
python -m unittest discover -s tests -v
```

## GitHub Pages

Publique o conteúdo gerado em `dist/`. Uma pipeline do GitHub Actions poderá executar `node build.mjs` usando variáveis configuradas no repositório. Os arquivos usam caminhos relativos para funcionar em subcaminhos.
