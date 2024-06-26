import styled, { css } from "styled-components";

const Row = styled.div`
  display: flex;
  gap: 1.6rem;

  ${(props) =>
    props.type === "filled" &&
    css`
      & > * {
        flex: 1 1 0;
      }
    `}
  ${(props) =>
    props.type === "splitted" &&
    css`
      align-items: center;
      justify-content: space-between;
    `}
  ${(props) =>
    props.type === "vertical" &&
    css`
      flex-direction: column;
    `}
`;

Row.defaultProps = {
  type: "horizontal",
};

export default Row;
