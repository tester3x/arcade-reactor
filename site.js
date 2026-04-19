// Arcade Reactor — site.js
// Mock high-score data. Swap with real backend data when the API lands.

const MOCK_LEADERBOARD = [
    { player: 'NEOVEC',  game: 'Space Rocks', score: 125400 },
    { player: 'ROCKET',  game: 'Space Rocks', score: 98720  },
    { player: 'PULSAR',  game: 'Space Rocks', score: 87300  },
    { player: 'ORBIT_7', game: 'Space Rocks', score: 64850  },
    { player: 'GLITCH',  game: 'Space Rocks', score: 51200  },
    { player: 'VOID',    game: 'Space Rocks', score: 44180  },
    { player: 'CRT_KID', game: 'Space Rocks', score: 38040  }
];

function formatScore(n) {
    return n.toLocaleString('en-US');
}

function renderLeaderboard() {
    const host = document.getElementById('leaderboard-rows');
    if (!host) return;
    host.innerHTML = MOCK_LEADERBOARD.map((row, i) => {
        const rank = i + 1;
        return `
            <li class="board-row rank-${rank}">
                <span class="board-rank">${String(rank).padStart(2, '0')}</span>
                <span class="board-player">${row.player}</span>
                <span class="board-game">${row.game}</span>
                <span class="board-score">${formatScore(row.score)}</span>
            </li>
        `;
    }).join('');
}

function setYear() {
    const el = document.getElementById('year');
    if (el) el.textContent = new Date().getFullYear();
}

document.addEventListener('DOMContentLoaded', () => {
    renderLeaderboard();
    setYear();
});
