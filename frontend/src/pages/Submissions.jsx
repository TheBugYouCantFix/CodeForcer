import Heading from "../ui/Heading.jsx";
import Form from "../ui/Form.jsx";
import Input from "../ui/Input.jsx";
import FormElement from "../ui/FormElement.jsx";
import Button from "../ui/Button.jsx";
import { SiCodeforces } from "react-icons/si";
import { useForm } from "react-hook-form";
import { useRef, useState } from "react";
import axios from "axios";
import SumbissionInfo from "../ui/SumbissionInfo.jsx";

function Handles() {
  const ref = useRef(null);
  const [contestInfo, setContestInfo] = useState({});

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const onSubmit = function (data) {
    axios
      .get(data.contestUrl)
      .then((response) => setContestInfo(response.data));
  };

  return (
    <>
      <Heading as="h1">
        <SiCodeforces />
        Download Submissions
      </Heading>

      {Object.keys(contestInfo).length === 0 && (
        <Form onSubmit={handleSubmit(onSubmit)}>
          <FormElement label="Contest URL">
            <Input
              defaultValue={
                "https://13bd4039-c465-4f54-b961-30824dc7cc9b.mock.pstmn.io/contests/52"
              }
              placeholder="id or full link"
              {...register("contestUrl")}
            />
          </FormElement>
          <FormElement label="Codeforces API">
            <Input placeholder="API Key" {...register("api-key")} />
            <Input placeholder={"Secret Key"} {...register("secret-key")} />
          </FormElement>
          <Button as="input" type="submit" value="Submit" />
        </Form>
      )}

      {Object.keys(contestInfo).length !== 0 && (
        <SumbissionInfo {...contestInfo} />
      )}
    </>
  );
}

export default Handles;
