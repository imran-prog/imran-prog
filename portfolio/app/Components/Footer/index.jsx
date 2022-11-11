import Link from "next/link";
import styles from "./Footer.module.sass";

export default function Footer() {
  return (
    <div className={styles.wrapper}>
      <p>Welcome to a newbie room</p>
      <h2>Imran Akbar</h2>
      <ul className={styles.menu_item}>
        <li>
          <button>About Me</button>
        </li>
        <li>
          <button>Projects</button>
        </li>
        <li>
          <button>Art</button>
        </li>
        <li>
          <button>Hobbies</button>
        </li>
        <li>
          <button>contact</button>
        </li>
      </ul>
      <ul className={styles.social_item}>
        <li>
          <div></div>
        </li>
        <li>
          <div></div>
        </li>
        <li>
          <div></div>
        </li>
        <li>
          <div></div>
        </li>
        <li>
          <div></div>
        </li>
      </ul>
    </div>
  );
}
