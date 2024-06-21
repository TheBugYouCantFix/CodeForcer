import Row from "../ui/Row.jsx";
import Heading from "../ui/Heading.jsx";
import Card from "../ui/Card.jsx";
import { HiHome } from "react-icons/hi2";
import { SiMoodle, SiCodeforces } from "react-icons/si";
import { FaDatabase } from "react-icons/fa6";

function Home() {
  return (
    <>
      <Heading as="h1">
        <HiHome />
        Home page
      </Heading>
      <Row type="filled">
        <Card title="Submit Grades" icon={SiMoodle} to="/submit" />
        <Card
          title="Download Submissions"
          icon={SiCodeforces}
          to="/submissions"
        />
        <Card title="Edit Handles" icon={FaDatabase} to="/handles" />
      </Row>
    </>
  );
}

export default Home;
