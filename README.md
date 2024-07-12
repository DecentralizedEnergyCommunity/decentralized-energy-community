# Decentralized Energy Comunity

Install the mise tool this is used to install the other tools:
https://mise.jdx.dev/getting-started.html
```
curl https://mise.run | sh
echo 'eval "$(~/.local/bin/mise activate bash)"' >> ~/.bashrc
echo 'eval "$(~/.local/bin/mise activate zsh)"' >> ~/.zshrc
```

Then the rest of the tools can be installed using:
```commandline
mise install -y
just setup
```