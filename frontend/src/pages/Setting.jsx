import Heading from "../ui/Heading.jsx";
import { TbSettingsFilled } from "react-icons/tb";
import { Description } from "../ui/Description.jsx";
import SumbissionsInfo from "../ui/SumbissionInfo.jsx";
import { useLoaderData, useNavigation } from "react-router-dom";
import { getContest } from "../api/contests.js";

export async function loader({ request, params }) {
  try {
    const contest = await getContest(
      params.contestId,
      JSON.parse(localStorage.getItem("api")),
      JSON.parse(localStorage.getItem("key")),
    );
    return { contest };
  } catch (err) {
    throw err;
  }
}

function Settings() {
  const { contest } = useLoaderData();
  const navigation = useNavigation();

  return (
    <>
      <Heading as="h1">
        <TbSettingsFilled />
        Set up the contest
      </Heading>
      <Description>
        <p>
          On this page you can upload the participants' results in .csv file
          <br />
          To do this, specify the maximum number of points for each task <br />
        </p>
        <p>You can also copy the list of undefined participants</p>
      </Description>
      <SumbissionsInfo info={contest} />
    </>
  );
}

export default Settings;
