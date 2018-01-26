import opt from "./cli-args";
import startServer from "./server";

const CONFIG = {};
const argv = opt.argv;

CONFIG.PORT_NUMBER = argv.p;
CONFIG.AUTO_OPEN_BROWSER = !argv.n;
CONFIG.BROWSER_NAME = argv.b || undefined;

startServer(CONFIG);
