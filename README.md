**Public DNS Manager**

Automate your Cloudflare DNS updates effortlessly with this Python script. Designed for both Ubuntu (nohup) and Windows environments, it dynamically fetches your public IP and updates A/CNAME records seamlessly. Configuration is straightforward, making dynamic DNS management a breeze.

---

**Usage:**

1. Clone the repository.
2. Configure o token da API Cloudflare e os detalhes do domínio em `config.json`.
3. Run on Ubuntu: `nohup python public_dns_manager.py &`
4. Run on Windows: Double-click or use the command prompt.

Enjoy hassle-free dynamic DNS updates!

---

**Requirements:**

- Python 3.x
- Install `requests` library: `pip install requests`
- Install `schedule` library: `pip install schedule`

**Contributions:**

Contributions are welcome! Fork the repository and submit pull requests for improvements.

**License:**

This project is open-source under the MIT License. See [LICENSE](LICENSE) for details.

---

*Enhance your DNS management with Public DNS Manager - a lightweight, cross-platform solution for automated Cloudflare DNS updates.*
