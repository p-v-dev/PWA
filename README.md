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

O workflow `.github/workflows/deploy-pages.yml` publica o site em `https://p-v-dev.github.io/PWA/` a cada push na `main` ou por execução manual.

1. Acesse **Settings > Secrets and variables > Actions > Variables**.
2. Crie as Repository Variables `CONTACT_WHATSAPP_NUMBER`, `CONTACT_WHATSAPP_MESSAGE`, `CONTACT_INSTAGRAM`, `CONTACT_PHONE`, `CONTACT_EMAIL`, `CONTACT_BUSINESS_HOURS` e `CONTACT_MAPS_URL`.
3. Acesse **Settings > Pages** e selecione **GitHub Actions** em **Source**.
4. Envie a alteração para a `main` ou execute manualmente o workflow em **Actions > Deploy GitHub Pages**.

Somente `CONTACT_WHATSAPP_NUMBER` é obrigatória. Os demais contatos podem ficar vazios e não aparecerão no site. Esses valores são públicos no site gerado, por isso devem ser Repository Variables, não Secrets.
