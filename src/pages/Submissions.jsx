import Heading from "../ui/Heading.jsx";
import Form from "../ui/Form.jsx";
import Input from "../ui/Input.jsx";
import FileInput from "../ui/FileInput.jsx";
import FormElement from "../ui/FormElement.jsx";
import Button from "../ui/Button.jsx";
import { SiCodeforces } from "react-icons/si";
import { useForm } from "react-hook-form";
import { useRef } from "react";

function Handles() {
  const ref = useRef(null);

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm();

  const watchFileInput = watch("file");

  const onSubmit = (data) => console.log(data);

  return (
    <>
      <Heading as="h1">
        <SiCodeforces />
        Download Submissions
      </Heading>
      <Form onSubmit={handleSubmit(onSubmit)}>
        <FormElement label="Contest URL">
          <Input placeholder="id or full link" {...register("contest-link")} />
        </FormElement>
        <FormElement label="Codeforces API">
          <Input placeholder="API Key" {...register("api-key")} />
          <Input placeholder={"Secret Key"} {...register("secret-key")} />
        </FormElement>
        <Button as="input" type="submit" value="Submit" />
      </Form>
    </>
  );
}

export default Handles;
