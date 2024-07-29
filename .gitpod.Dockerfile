FROM gitpod/workspace-full

RUN <<EOR
# Notify about jupyter server on SSH or xtermjs

cat >>"$HOME/.bashrc" <<'BASH'
if test ! -v TMUX && (test -v SSH_CONNECTION || test "$PPID" == "$(pgrep -f '/ide/xterm/bin/node /ide/xterm/index.cjs' | head -n1)"); then {
    # if pgrep jupyter 1>/dev/null; then {
        printf '%s' "INFO: Waiting for Jupyter server in a task terminal: "
        gp ports await 8888
    # } fi
} fi
BASH

EOR
