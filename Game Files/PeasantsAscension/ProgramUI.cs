using Classes.Units;
using Methods;

namespace PeasantsAscension
{
    public class ProgramUI
    {

        public void Run()
        {
            PlayableCharacter player = new PlayableCharacter("Stewson");
            Battle.BattleSystem();
        }
    }
}
