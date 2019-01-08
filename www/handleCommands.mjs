/**
 * Executes a command
 * @param {string} command The command you want to define
 */
export default command => {
  switch (command) {
    case "clean":
      const messages = document.querySelectorAll("main>div");
      for (const message of messages) {
        message.remove();
      }
      // @ts-ignore
      document.getElementById("scroll-message").close();
      break;
  }
};
