using Microsoft.AspNetCore.Cors;
using Microsoft.AspNetCore.Mvc;
using Model;
using Persistence;

namespace REST_Services.Controllers.Api;

[EnableCors("AllowSpecificOrigin")]
[ApiController]
[Route("api/zboruri")]
public class ZboruriController(IZboruriRepository zboruriRepository) : ControllerBase
{
    [HttpGet]
    public ActionResult<List<Zbor>> GetAll([FromQuery] string dest = null, [FromQuery] DateTime date = default,
        [FromQuery] int min = 0)
    {
        if (dest != null && date != default && min != 0)
            return Ok(zboruriRepository.FindAllByDestDateAndMinimumSeats(dest, date, min));
        return Ok(zboruriRepository.FindAll().ToList());
    }

    [HttpGet("{id}")]
    public ActionResult<Zbor> GetById(int id)
    {
        var zbor = zboruriRepository.FindOne(id);
        if (zbor == null)
        {
            return NotFound();
        }

        return Ok(zbor);
    }

    [HttpPost]
    public ActionResult<Zbor> Create([FromBody] Zbor zbor)
    {
        var createdModel = zboruriRepository.Save(zbor);
        return CreatedAtAction(nameof(GetById), new { id = createdModel.Id }, createdModel);
    }

    [HttpPut("{id}")]
    public ActionResult<Zbor> Update(int id, [FromBody] Zbor zbor)
    {
        if (id != zbor.Id)
        {
            return BadRequest();
        }

        var existingModel = zboruriRepository.FindOne(id);
        if (existingModel == null)
        {
            return NotFound();
        }

        zboruriRepository.Update(id, zbor);
        return NoContent();
    }

    [HttpDelete("{id}")]
    public ActionResult Delete(int id)
    {
        var existingModel = zboruriRepository.FindOne(id);
        if (existingModel == null)
        {
            return NotFound();
        }

        zboruriRepository.Delete(id);
        return NoContent();
    }
}