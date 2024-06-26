import styled, { css } from "styled-components";
import Heading from "./Heading.jsx";
import Row from "./Row.jsx";

const sumbissionType = {
  OK: css`
    & div:first-child {
      color: var(--color-brand-600);
    }
  `,
  FAILED: css`
    & div:first-child {
      color: var(--color-red-700);
    }
  `,
  REJECTED: css`
    & div:first-child {
      color: var(--color-yellow-700);
    }
  `,
};

const StyledCover = styled.div`
  display: flex;
  flex-direction: column;
  gap: 3.6rem;

  text-align: center;
  color: var(--color-grey-600);
  font-size: 1.6rem;
  font-weight: 500;
  padding: 3rem 4.5rem;
  transition: all 0.3s;
  box-shadow: var(--shadow-md);
  border-radius: var(--border-radius-md);
`;

const Item = styled.div`
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  row-gap: 1.5rem;
`;

const ItemContent = styled.div`
  max-width: 100%;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  column-gap: 1.5rem;
  row-gap: 2rem;
`;

const ParticipantInfo = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
  padding-left: 0.9em;
  text-align: left;
  align-items: flex-start;
  font-size: 1.4rem;
  padding: 1rem 2.5rem;
  padding-right: 1.5rem;
  box-shadow: var(--shadow-md);
  border-radius: var(--border-radius-md);
  white-space: dots;

  & div {
    list-style-type: disc;
    text-overflow: dots;
  }

  ${(props) => sumbissionType[props.type]}
`;
function SumbissionInfo({ name, preparedBy, problems }) {
  return (
    <StyledCover>
      <Heading as="h2">Contest "{name}"</Heading>
      <Row direction="horizontal" style={{ alignSelf: "center" }}>
        <p>
          Prepared by: <strong>{preparedBy}</strong>
        </p>
        <p>
          Total number of problems: <strong>{problems.length}</strong>
        </p>
      </Row>
      {problems.map((item, index) => (
        <Item key={index}>
          <p>Problem: {item.index}</p>
          {item.submissions ? (
            <ItemContent>
              {item.submissions.map((item, index) => (
                <ParticipantInfo key={index} type={item.verdict}>
                  <div>{item.authorId}</div>
                  <div>{item.programmingLanguage}</div>
                  <div>{item.points}</div>
                </ParticipantInfo>
              ))}
            </ItemContent>
          ) : (
            <p>No one was able to provide solutions</p>
          )}
        </Item>
      ))}
    </StyledCover>
  );
}

export default SumbissionInfo;
