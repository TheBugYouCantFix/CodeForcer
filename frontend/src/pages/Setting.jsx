import Heading from "../ui/Heading.jsx";
import { TbSettingsFilled } from "react-icons/tb";
import { Description } from "../ui/Description.jsx";
import SumbissionsInfo from "../ui/SumbissionInfo.jsx";

function Settings() {
  return (
    <>
      <Heading as="h1">
        <TbSettingsFilled />
        Set up the contest
      </Heading>
      <Description>
        <p>
          On this page you can specify the maximum points for each task on
          moodle
        </p>
      </Description>
      <SumbissionsInfo />
    </>
  );
}

export default Settings;
